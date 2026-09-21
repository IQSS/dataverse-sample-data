#!/usr/bin/env python3
"""
create_sample_big_batch_dataset.py: Ingest or generate large batches of sample files for Dataverse performance testing.

Features:
- Fast lightweight file generation (no heavy CairoSVG/system C-library dependency required).
- Supports batch ingestion with configurable batch size and delay (replicating DVUploader or bulk migration workloads).
- Real-time latency tracking, throughput reporting, and degradation analysis (first 10% vs last 10% latency).
- Dual mode:
  1. Direct Upload Mode (default): Ingests files directly into Dataverse in batches via API.
  2. Local Generation Mode (--generate-only): Generates files on disk into the sample-data directory structure.
"""

import argparse
import io
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


# Minimal 1x1 transparent GIF (43 bytes)
TINY_GIF_BYTES = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"


def get_default_config():
    default_base_url = "http://localhost:8080"
    default_api_token = ""
    try:
        import dvconfig
        default_base_url = getattr(dvconfig, "base_url", default_base_url)
        default_api_token = getattr(dvconfig, "api_token", default_api_token)
    except ImportError:
        pass

    base_url = os.environ.get("DATAVERSE_URL", os.environ.get("BASE_URL", default_base_url))
    api_token = os.environ.get("API_TOKEN", os.environ.get("DATAVERSE_API_KEY", default_api_token))
    return base_url, api_token


def parse_args():
    default_base_url, default_api_token = get_default_config()

    parser = argparse.ArgumentParser(
        description="Ingest or generate large batches of sample files for Dataverse performance testing."
    )
    parser.add_argument(
        "--url",
        default=default_base_url,
        help=f"Dataverse base URL (default: {default_base_url}, or $DATAVERSE_URL)",
    )
    parser.add_argument(
        "--api-token",
        default=default_api_token,
        help="Dataverse API token (default: from dvconfig.py or $API_TOKEN)",
    )
    parser.add_argument(
        "--total-files",
        type=int,
        default=100,
        help="Total number of files to generate/upload (default: 100)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size before delay (default: 50)",
    )
    parser.add_argument(
        "--batch-delay",
        type=float,
        default=1.0,
        help="Delay in seconds between batches (default: 1.0s, replicating DVUploader pacing)",
    )
    parser.add_argument(
        "--file-type",
        choices=["txt", "gif", "mixed"],
        default="txt",
        help="Sample file format to generate: txt, gif, or mixed (default: txt)",
    )
    parser.add_argument(
        "--dataset-id",
        type=int,
        default=None,
        help="Target Dataset numeric ID (creates or discovers performance-test dataset by default)",
    )
    parser.add_argument(
        "--dataset-pid",
        default=None,
        help="Target Dataset persistent identifier (e.g. doi:10.5072/FK2/...)",
    )
    parser.add_argument(
        "--dataverse",
        default="dataverse-performance-demo",
        help="Parent dataverse alias if creating a new dataset (default: dataverse-performance-demo)",
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only generate files on disk into the performance-test directory, do not upload directly",
    )
    parser.add_argument(
        "--output-dir",
        default="./data/dataverses/dataverse-performance-demo/datasets/performance-test/files",
        help="Target directory for --generate-only mode",
    )
    return parser.parse_args()


def generate_file_content(idx, file_type):
    is_gif = (file_type == "gif") or (file_type == "mixed" and idx % 2 == 0)
    if is_gif:
        filename = f"batch_file_{idx:06d}.gif"
        content = TINY_GIF_BYTES
        mime = "image/gif"
    else:
        filename = f"batch_file_{idx:06d}.txt"
        content = (
            f"Dataverse sample data batch file index {idx:06d}\n"
            f"Created: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n"
            f"Payload: {'X' * 64}\n"
        ).encode("utf-8")
        mime = "text/plain"
    return filename, content, mime


def run_generate_only(total_files, file_type, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Generating {total_files} lightweight sample files in: {output_dir}")
    t0 = time.time()
    for idx in range(1, total_files + 1):
        filename, content, _ = generate_file_content(idx, file_type)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        if idx % 1000 == 0 or idx == total_files:
            print(f"  [Generated {idx}/{total_files} files]")
    elapsed = time.time() - t0
    print(f"[+] Successfully generated {total_files} files in {elapsed:.2f}s ({total_files/max(elapsed, 0.001):.1f} files/s).")
    print("    You can now run 'python create_sample_data.py' to ingest them into Dataverse.")


def get_or_create_dataset(base_url, api_token, dataverse_alias, dataset_pid=None, dataset_id=None):
    headers = {"X-Dataverse-key": api_token}

    if dataset_id:
        return dataset_id

    if dataset_pid:
        r = requests.get(f"{base_url.rstrip('/')}/api/datasets/:persistentId/?persistentId={dataset_pid}", headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json()["data"]["id"]

    # Check if target dataverse exists; if not, create it
    dv_url = f"{base_url.rstrip('/')}/api/dataverses/{dataverse_alias}"
    r_dv = requests.get(dv_url, headers=headers, timeout=30)
    if r_dv.status_code == 404:
        print(f"[*] Dataverse '{dataverse_alias}' not found. Creating it under ':root'...")
        dv_payload = {
            "name": "Dataverse performance demo",
            "alias": dataverse_alias,
            "dataverseContacts": [{"contactEmail": "dataverse-sample-data@mailinator.com"}],
            "description": "Demo collection for performance testing",
            "dataverseType": "RESEARCH_PROJECTS"
        }
        r_create_dv = requests.post(f"{base_url.rstrip('/')}/api/dataverses/:root", headers=headers, json=dv_payload, timeout=30)
        if r_create_dv.status_code not in (200, 201):
            print(f"[!] Warning creating dataverse: {r_create_dv.status_code} - {r_create_dv.text}")

    # Create a dedicated performance test dataset
    print(f"[*] Creating a new performance test dataset under '{dataverse_alias}'...")
    ds_payload = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "title",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": f"Big Batch Performance Test Dataset ({int(time.time())})"
                        },
                        {
                            "typeName": "author",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [{"authorName": {"typeName": "authorName", "multiple": False, "typeClass": "primitive", "value": "SampleData, Benchmark"}}]
                        },
                        {
                            "typeName": "datasetContact",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [{
                                "datasetContactName": {"typeName": "datasetContactName", "multiple": False, "typeClass": "primitive", "value": "Benchmark Runner"},
                                "datasetContactEmail": {"typeName": "datasetContactEmail", "multiple": False, "typeClass": "primitive", "value": "dataverse-sample-data@mailinator.com"}
                            }]
                        },
                        {
                            "typeName": "dsDescription",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [{"dsDescriptionValue": {"typeName": "dsDescriptionValue", "multiple": False, "typeClass": "primitive", "value": "Automated dataset created to evaluate big batch upload and ingestion performance."}}]
                        },
                        {
                            "typeName": "subject",
                            "multiple": True,
                            "typeClass": "controlledVocabulary",
                            "value": ["Other"]
                        }
                    ]
                }
            }
        }
    }
    r_create_ds = requests.post(f"{base_url.rstrip('/')}/api/dataverses/{dataverse_alias}/datasets", headers=headers, json=ds_payload, timeout=30)
    r_create_ds.raise_for_status()
    data = r_create_ds.json()["data"]
    created_id = data["id"]
    created_pid = data.get("persistentId", "N/A")
    print(f"[+] Created performance test dataset ID: {created_id} (PID: {created_pid})")
    return created_id


def run_batch_upload(base_url, api_token, dataset_id, total_files, batch_size, batch_delay, file_type):
    upload_url = f"{base_url.rstrip('/')}/api/datasets/{dataset_id}/add"
    headers = {"X-Dataverse-key": api_token}

    print(f"\n{'='*75}")
    print(f"Starting Big Batch Ingestion: {total_files} files in batches of {batch_size}")
    print(f"Target Endpoint: {upload_url}")
    print(f"Inter-batch Delay: {batch_delay}s")
    print(f"{'='*75}\n")

    latencies = []
    batch_latencies = []
    total_start_time = time.time()

    for idx in range(1, total_files + 1):
        filename, content, mime = generate_file_content(idx, file_type)
        files = {
            "file": (filename, content, mime),
            "jsonData": (None, json.dumps({"description": f"Batch file {idx}"}), "application/json")
        }

        t_start = time.time()
        res = requests.post(upload_url, headers=headers, files=files, timeout=120)
        t_end = time.time()

        if res.status_code not in (200, 201):
            print(f"[!] Error on file #{idx}: HTTP {res.status_code} - {res.text}")
            continue

        latency = t_end - t_start
        latencies.append(latency)
        batch_latencies.append(latency)

        # Log progress every 10 files or at batch boundaries
        if idx % 10 == 0 or idx == total_files:
            avg_recent = sum(batch_latencies) / len(batch_latencies)
            throughput_recent = len(batch_latencies) / max(sum(batch_latencies), 0.001)
            print(f"  [#{idx:05d}/{total_files:05d}] Latency: {latency:.3f}s | Batch Avg: {avg_recent:.3f}s | Speed: {throughput_recent:.1f} files/s")
            batch_latencies = []

        # Batch boundary pause (replicates DVUploader and prevents server DOS)
        if idx % batch_size == 0 and idx < total_files:
            print(f"  [*] Batch of {batch_size} finished. Pausing {batch_delay:.1f}s...")
            time.sleep(batch_delay)

    total_duration = time.time() - total_start_time
    print_summary(latencies, total_duration, total_files)


def print_summary(latencies, total_duration, total_requested):
    print(f"\n{'='*75}")
    print("BIG BATCH INGESTION SUMMARY & METRICS")
    print(f"{'='*75}")
    n = len(latencies)
    if n == 0:
        print("[!] No files were successfully uploaded.")
        return

    sample_k = max(1, n // 10)
    first_avg = sum(latencies[:sample_k]) / sample_k
    last_avg = sum(latencies[-sample_k:]) / sample_k
    ratio = last_avg / max(first_avg, 0.0001)

    print(f"Files successfully uploaded: {n} / {total_requested}")
    print(f"Total time elapsed:         {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    print(f"Overall throughput:          {n/max(total_duration, 0.001):.2f} files/second")
    print(f"Min latency:                 {min(latencies):.3f}s")
    print(f"Max latency:                 {max(latencies):.3f}s")
    print(f"Mean latency:                {sum(latencies)/n:.3f}s")
    print(f"First 10% average latency:   {first_avg:.3f}s (files 1..{sample_k})")
    print(f"Last 10% average latency:    {last_avg:.3f}s (files {n - sample_k + 1}..{n})")
    print(f"Degradation ratio:           {ratio:.2f}x")

    print("\n--- HEALTH DIAGNOSTIC ---")
    if ratio < 1.5:
        print("  ✓ EXCELLENT (O(1) Scaling): Upload latency remained steady across the entire ingestion run.")
    elif ratio < 2.5:
        print("  - MODERATE: Minor latency increase, typical under concurrent indexing or garbage collection.")
    else:
        print("  ⚠ DEGRADATION DETECTED: Upload latency increased significantly (>2.5x).")
        print("    If running Dataverse <= 6.12 without PR #12729, check for O(N) database UPDATE cascades.")
    print(f"{'='*75}\n")


def main():
    args = parse_args()

    if args.generate_only:
        run_generate_only(args.total_files, args.file_type, args.output_dir)
        return

    if not args.api_token:
        print("[!] Error: Dataverse API token is required. Specify via --api-token, $API_TOKEN env var, or dvconfig.py.")
        sys.exit(1)

    dataset_id = get_or_create_dataset(args.url, args.api_token, args.dataverse, args.dataset_pid, args.dataset_id)
    run_batch_upload(
        base_url=args.url,
        api_token=args.api_token,
        dataset_id=dataset_id,
        total_files=args.total_files,
        batch_size=args.batch_size,
        batch_delay=args.batch_delay,
        file_type=args.file_type,
    )


if __name__ == "__main__":
    main()

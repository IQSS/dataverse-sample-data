The sole purpose of this file is to illustrate how to add an access-restricted file 
to the sample data collection. 
The restriction is set in the optional JSON file metadata fragment (the format is modeled
under the standard JSON output of the file fragment in the Dataverse API output of the 
/api/datasets/.../version, and similar endpoints). 
For example, for this file the file metadata fragment open-source-at-harvard/.filemetadata/README_private.txt looks as follows:

{
   "description": "The sole purpose of this file is to illustrate access restriction",
   "restricted": true,
   "categories":
      [
         "Documentation"
      ]
}

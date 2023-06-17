# Optifine API
This unofficial Flask API allows to interact with Optifine services more easily. It is currently WIP.

## Usage

### Get versions
```
GET /versions
```
Returns a list of all versions in a json array.

### Download
```
GET /download/?link=<link>
```
Downloads the file from the link and returns it. The link must be a 'adloadx' link.

Example: `/download/?link=http://optifine.net/adloadx?f=OptiFine_1.19.4_HD_U_I4.jar` will return a direct download link to the jar file.
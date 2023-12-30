# GCP README

In order to use GCP resources, you will need to download a JSON credentials package from the GCP console.  That text file will need to be read into the `gcp_service_account` variable when running playbooks that call this role.  There are many ways to do this, but the following is an example of retrieving that file from the filesystem and JSON encoding it.

```bash
ansible-navigator run lab.osbuild.gcp_setup \
-i inventory \
-l localhost \
--pae false \
--mode stdout \
--lf /dev/null \
--ee false \
--extra-vars "gcp_project='my-project'" \
--extra-vars "gcp_bucket=my-bucket" \
--extra-vars "gcp_service_account={{ lookup('file', '~/.service_account.json') | to_json }}" \
-vv
```

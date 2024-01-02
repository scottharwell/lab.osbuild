# lab.osbuild A Collection to build Ansible cloud VM images based on RHEL

## Introduction

The Ansible on Clouds team has a need to publish VM images that contain the Ansible installer packaged with a standard RHEL base image.  This repository implements examples for creating that image.

This project is a proof of concept to include the Ansible Automation Platform repos into the main `osbuild` available repos with the respective RHSM (Red Hat Subscription Manager).

Reference the [osbuild docs][os_build_docs] for information about the files and commands that this collection runs in order to prepare and queue build processes.

## Instructions

### Prepare your accounts

The build process will require that you have an active Red Hat account that may be used to login to `registry.redhat.io`.  

Each cloud requires certain permissions and roles for uploading files to storage and creating machine images.  The [osbuild docs][cloud_images] have information about the credential requirements for preparing the clouds.  This collection also has playbooks for preparing each cloud with object storage for building images.

#### AWS Setup

If you are pushing images to AWS, this collection has a playbook that will setup the proper resources to deploy images.  View the defaults in the role's defaults file `roles/aws/defaults/main.yml`.  Change any variable either inline when running the playbook, or in a vars file like in the example below.

```bash
ansible-navigator run lab.osbuild.aws_setup \
-i env/inventory \
--pae false \
--mode stdout \
--lf /dev/null \
--ee false \
--extra-vars "@env/vars.yml"
```

#### Azure Setup

If you are pushing images to Azure, this collection has a playbook that will setup the proper resources to deploy images.  View the defaults in the role's defaults file `roles/azure/defaults/main.yml`.  Change any variable either inline when running the playbook, or in a vars file like in the example below.

```bash
ansible-navigator run lab.osbuild.azure_setup \
-i env/inventory \
--pae false \
--mode stdout \
--lf /dev/null \
--ee false \
--extra-vars "@env/vars.yml"
```

### Prepare the local machine

Install this collection onto your local machine so that calling the fully-qualified playbook name will work.

```bash
ansible-galaxy collection install git+https://github.com/scottharwell/osbuild-with-rhsm-repos.git
```

Next, create a vars file to configure variables that can be saved to the filesystem.  You can pass the secrets in via credentials, env vars, or other secrets management at run time.

```yaml
---
composer_build_image_version: "1.0.0"
composer_add_epel_repo: true
composer_clouds:
  - name: azure
    image_format: vhd
    storage_container_name: vmimagecontainer
    storage_account_name: "{{ azure_storage_account_name }}"
    storage_account_access_key: "{{ azure_storage_account_access_key }}"
  - name: aws
    image_format: ami
    region: us-east-1
    bucket: aoc-vm-image-imports
    image_key: "{{ composer_image_key }}"
    access_key_id: "{{ aws_access_key_id }}"
    secret_access_key: "{{ aws_secret_access_key }}"
    session_token: "{{ aws_session_token | default(None) }}"
```

Create a local inventory file to connect to your RHEL builder machine.

```ini
[builder]
builder.host.your.domain
```

### Prepare Build Machine

This collection assumes that you have a RHEL 9 machine that will act as a build host for the images.  You will need both an `x86_64` and an `aarch64` build machines if you intend to build different architectures.

The playbooks included in this collection will allow you to prepare that RHEL host and then deploy a VM image.  The following must be performed on the build machine prior to using this playbook.

* The OS must be RHEL 9
* RHEL should have subscription manager registered and attached with valid RHEL entitlements
* You must use a Red Hat subscription with access to the Ansible Automation Platform repositories; either a developer account or an account that has purchased AAP.

You should now be ready to run the playbook that will prepare your RHEL host with Image Builder and dependencies.  No extra vars should be required for this playbook.

```bash
ansible-navigator run lab.osbuild.host_setup \
-i env/inventory \
--pae false \
--mode stdout \
--lf /dev/null \
--ee false \
--extra-vars "@env/vars.yml" \
-vv
```

### Build Image

The `build_images` playbook currently builds images based on the files in the `roles/composer/templates/` folder.  Each cloud has a slightly different setup.  Changes to that templates will result in changes to the build image.

The `composer_clouds` variable will determine which images are built.  Remove or comment a particular cloud from the list if you do not want to deploy to that cloud.  If a cloud is removed, the variables specific to that cloud are not required; for instance, the example below will build Azure and AWS images, but not GCP or OCI.  See the `roles/composer/defaults/main.yml` file for the variables required for each cloud.

```yaml
composer_clouds:
  - name: azure
    image_format: vhd
    storage_container_name: vmimagecontainer
    storage_account_name: "{{ azure_storage_account_name }}"
    storage_account_access_key: "{{ azure_storage_account_access_key }}"
  - name: aws
    image_format: ami
    region: us-east-1
    bucket: aoc-vm-image-imports
    image_key: "{{ composer_image_key }}"
    access_key_id: "{{ aws_access_key_id }}"
    secret_access_key: "{{ aws_secret_access_key }}"
    session_token: "{{ aws_session_token | default(None) }}"
```

You will also need to prepare environment variables that will pass the secrets required for this operation.  Those are identified in the command below.  The secrets values are stored in configuration files for the composer-cli on the Image Builder host.  If you are using temporary credentials, such as an AWS Session Token, then current builds may work and later builds fail when the session expires.  You will either need to run the `build_images` playbook during your next build to ensure valid credentials, or use static credentials that are longer lived.

```bash
ansible-navigator run lab.osbuild.build_images \
-i env/inventory \
--pae false \
--mode stdout \
--lf /dev/null \
--ee false \
--extra-vars "podman_username=$RED_HAT_ACCOUNT" \
--extra-vars "podman_password='$RED_HAT_PASSWORD'" \
--extra-vars "azure_storage_account_name='$AZURE_STORAGE_ACCOUNT_NAME'" \
--extra-vars "azure_storage_account_access_key='$AZURE_STORAGE_ACCOUNT_KEY'" \
--extra-vars "aws_access_key_id='$AWS_ACCESS_KEY_ID'" \
--extra-vars "aws_secret_access_key='$AWS_SECRET_ACCESS_KEY'" \
--extra-vars "aws_session_token='$AWS_SESSION_TOKEN'" \
--extra-vars "@env/vars.yml" \
-vv
```

### Unsupported Image Types

There are clouds and cloud image types that are not always supported.  For instance, the `gce` and `oci` types are not available in the `aarch64` version of image builder.  However, you can still use image builder to build ARM images for these platforms.  You can follow these steps, generically, to build an image for any platform.  These steps will create an ARM image for Google Cloud.

1. Run the `lab.osbuild.build_images` playbook with the `gcp` cloud configuration.  This step will fail at built, but it will seed the GCP blueprint and all other required files into the VM hosting image builder.
2. SSH into the image builder host.
3. Run the following command to create a `qcow2` image.

    ```bash
    composer-cli compose start gcp qcow2 --size 4096
    ```

4. Check the build process using the following command.

    ```bash
    composer-cli compose list
    ```

5. Once the build has completed, run the following command to export the image.

    ```bash
    composer-cli compose image <uuid of the image>
    ```

6. If you have the Google Cloud CLI on your build manchine, then proceed to step 7.  Otherwise, copy this image file to the machine where the Google Cloud CLI is installed.
7. Run the following command to ensure that the disk image is in the correct format.

    ```bash
    qemu-img convert <uuid of the image>-disk.qcow2 -O raw disk.raw -p
    ```

8. The the following command to properly tar and gzip the file.  You may need to manually install the gnu-tar utility if on a Mac or distribution that does not provide the tar command with support for the `--format` flag.  `gtar` is used in this example as I use a mac and have to call the utility directly since macOS has a native version of the command.

    ```bash
    gtar -czvf "aap-installer-rhel9-aarch64-.tar.gz" --format=oldgnu disk.raw
    ```

9. Upload the image to object storage.

    ```bash
    gcloud storage cp aap-installer-rhel9-aarch64.tar.gz gs://<gcloud bucket name>
    ```

10. Use the Google Cloud CLI to create the image.  **Note:** You must use the CLI as the console does not support the proper flags to get the image in a running state for ARM processors.

    ```bash
    gcloud compute images create aap-installer-rhel9-aarch64 \
    --source-uri=gs://<gcloud bucket name>/aap-installer-rhel9-aarch64.tar.gz \
    --guest-os-features="UEFI_COMPATIBLE,GVNIC,VIRTIO_SCSI_MULTIQUEUE,SEV_CAPABLE,SEV_SNP_CAPABLE" \
    --architecture ARM64 \
    --family rhel-9
    ```

You now have an `aarch64` version of the machine image ready to run on compatible processors on Google Cloud.

[os_build_docs]: https://www.osbuild.org/guides/introduction.html
[cloud_images]: https://www.osbuild.org/guides/image-builder-on-premises/uploading-to-cloud.html

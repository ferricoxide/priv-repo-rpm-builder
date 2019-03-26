# About

This project is designed to facilitate the use of private Yum repositories for managing packages for CentOS-based systems. The primary contents are RPM SPEC files and templated source files.

The templated source files are derived from upstream CentOS and Fedora/EPEL yum repository definition (`*.repo`) files. The upstream files are downloaded, copied out from their source RPM and then modified to become template files.

The `.spec` files included in this project use simple `sed` filters to convert the template `*.repo` files into "real" `*.repo` files that point to private yum repositories. The "real" `*.repo` &ndash; along with any other relevant files typically included in the upstream files &ndash; are then packaged up as RPMs. These RPMs can then be signed, distributed and installed as appropriate for a given private network.

Systems with the requisite RPMs installed can then fetch from local/private yum repository-mirrors as though they were fetching packages from their Internet-hosted/public analogues.

## Usage

This project's file-layout is designed to foster the creation of RPMs. All RPM-related files are stored under the `<PROJECT_ROOT>/rpmbuild` directory-tree. The simplest method for creating RPMs is to do something like:

~~~
for SPEC in *.spec
do
   rpmbuild --define="_topdir <PROJECT_ROOT>/rpmbuild" \
     --define="my_privroot <REPO_ALIAS>" \
     --define "my_urlroot <REPO_HOST>" \
     --define="my_pathroot <REPO_PATH_ROOT>" -ba ${SPEC}
done
~~~

Where:

* `PROJECT_ROOT`: The fully-qualified path to this project as created by a `git clone` operation (e.g., `/home/user/private-centos-repos`)
* `REPO_ALIAS`: A short string to identify the internal repositories (e.g., `internal`)
* `REPO_HOST`: The fully-qualified domain name of the HTTP-reachable yum repository server (e.g. `my-repo.my.domin`)
* `REPO_PATH_ROOT`: The initial part of the repository-server URL's file-path (e.g., `centos` or `yum/centos`)

Once the `rpmbuild` operations complete, the resultant RPMs will be found in the `<PROJECT_ROOT>/rpmbuild/RPMS/noarch` directory. If local site policies require RPMs to be GPG-signed, do so. The (signed) RPMs can then be uploaded to an appropriate yum server &ndash; or other repository &ndash; for distribution to CentOS-based clients.

## Notes

Ensure that, if populating a yum server with the resultant RPMs, the yum server's metadata (and file-group definitions) are appropriately updated. Specifics for this are outside the scope of this document.

## Testing

### TravisCI

This project includes a `.travis.yml` file. Any time a commit &ndash; or group of commits &ndash; is pushed to GitHub, a test-job will be kicked off within the TravisCI service. This job:

1. Launches a build-host within TravisCI's environment
1. Installs and enables the Docker service
1. Downloads the GitHub project's contents to the build-host
1. Starts a CentOS 7 container from DockerHub, mapping the project contents into the container
1. Iterates over the various spec-files, and attempting to build throw-away RPMs

If RPMs are able to be created from each of the iterated spec-files, the test will return green. Failure to build from any given spec-file should cause the job to fail at the first-encountered build-error.

---

| Build Service | Build Status |
| ------------- | ------------ |
| TravisCI      | [![Build Status](https://travis-ci.com/ferricoxide/priv-repo-rpm-builder.svg?branch=master)](https://travis-ci.com/ferricoxide/priv-repo-rpm-builder) |

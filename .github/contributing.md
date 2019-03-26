# Background 

This project is designed to facilitate the creation of yum repository configuration RPMs to act as one-for-one analogs to those distributed for the CentOS and EPEL projects. The included SPEC files and template Private-*.repo files work together to allow builder to easily create yum repository configuration RPMs suitable for use on isolated networks that mirror the Internet-hosted original repositories.

If/when CentOS.Org or the Fedora/EPEL team publish new or updated repository definitions, it may be necessary to add further SPEC and template Private-*.repo files to this project. While the owners of this project endeavor to stay in sync with the upstream project, anyone that finds this project is welcome to fill in any gaps caused by the project-owners to fall behind the CentOS and/or Fedora/EPEL teams. To contribute, use existing SPEC files to guide the creation of new SPEC files.

Note: This project only contains the tools for creating RPMs, not the actual S/RPMs, themselves.

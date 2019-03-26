%define         privroot %{?my_privroot}%{?!my_privroot:private}
%define         urlroot %{?my_urlroot}%{?!my_urlroot:mirror.centos.org}
%define         pathroot %{?my_pathroot}%{?!my_pathroot:centos}
%define         MYBUILDIR %{name}-%{version}-%{release}

Name:		%{privroot}-release-gluster5
Version:	1.0
Release:	1%{?dist}
Summary:	Private network copy of Gluster 5 packages from the CentOS Storage SIG repository
Url:            http://mirror.centos.org/centos/7/extras/x86_64/Packages/centos-release-gluster5-%{version}-%{release}.noarch.rpm


Group:		System Environment/Base
License:	GPLv2

Source2:        Private-Gluster-5.repo


BuildArch:      noarch
BuildRequires:	rpm
Requires:	centos-release

Requires:       centos-release-storage-common
Provides:       centos-release-gluster = 5
Obsoletes:      centos-release-gluster < 5

%description
yum configuration for Gluster 5 packages from the CentOS Storage SIG.  Gluster
5 will receive updates for approximately 12 months. For more details about the
release and maintenance schedule, see
https://www.gluster.org/community/release-schedule



%prep
# Nuke stale build-dir
if [[ -d %{MYBUILDIR} ]]
then
   rm -rf %{MYBUILDIR}
fi

# Create new build-dir
install -Ddm 000755 %{MYBUILDIR}
install -Dbm 000644 %{SOURCE2} %{MYBUILDIR}



%build
sed -i '{
         s/__PRIVREPO__/%{privroot}/g
         s/__MIRROR_HOST__/%{urlroot}/g
         s#__PATH_ROOT__#%{pathroot}#g
         /baseurl/s/$/\nskip_if_unavailable=1/
      }' %{MYBUILDIR}/Private-Gluster-5.repo


%install
PRIVCAP=$( echo %{privroot} | tr "[:lower:]" "[:upper:]" )
install -Dbm 000644 %{MYBUILDIR}/Private-Gluster-5.repo %{buildroot}/%{_sysconfdir}/yum.repos.d/${PRIVCAP}-Gluster-5.repo

%files
%defattr(000644,root,root,000755)
%doc
%config /etc/yum.repos.d/*



%changelog

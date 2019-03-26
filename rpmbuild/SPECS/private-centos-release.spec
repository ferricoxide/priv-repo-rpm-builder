%define         privroot %{?my_privroot}%{?!my_privroot:private}
%define         urlroot %{?my_urlroot}%{?!my_urlroot:mirror.centos.org}
%define         pathroot %{?my_pathroot}%{?!my_pathroot:centos}
%define         MYBUILDIR %{name}-%{version}-%{release}

Name:		%{privroot}-release
Version:	7
Release:	6.1810.2%{?dist}
Summary:	Private network CentOS Linux release file
Url:            http://mirror.centos.org/centos/7/os/x86_64/Packages/centos-release-%{version}-%{release}.centos.x86_64.rpm

Group:		System Environment/Base
License:	GPLv2

Source1:	Private-Base.repo
Source2:        Private-CR.repo
Source3:        Private-Debuginfo.repo
Source4:        Private-Media.repo
Source5:        Private-Sources.repo
Source6:        Private-Vault.repo
Source7:        Private-fasttrack.repo

BuildArch:      noarch
BuildRequires:	rpm
Requires:	centos-release

%description
CentOS Linux release files


%prep
# Nuke stale build-dir
if [[ -d %{MYBUILDIR} ]]
then
   rm -rf %{MYBUILDIR}
fi

# Create new build-dir
install -Ddm 000755 %{MYBUILDIR}
install -bm 000644 %{SOURCE1} %{MYBUILDIR}
install -bm 000644 %{SOURCE2} %{MYBUILDIR}
install -bm 000644 %{SOURCE3} %{MYBUILDIR}
install -bm 000644 %{SOURCE4} %{MYBUILDIR}
install -bm 000644 %{SOURCE5} %{MYBUILDIR}
install -bm 000644 %{SOURCE6} %{MYBUILDIR}
install -bm 000644 %{SOURCE7} %{MYBUILDIR}



%build
PRIVCAP=$( echo %{privroot} | tr "[:lower:]" "[:upper:]" )
for FILE in %{MYBUILDIR}/*
do
   sed -i '{
         s/__PRIVREPO__/%{privroot}/g
         s/__MIRROR_HOST__/%{urlroot}/g
         s#__PATH_ROOT__#%{pathroot}#g
         /baseurl/s/$/\nskip_if_unavailable=1/
      }' $FILE
   mv ${FILE} ${FILE//Private-/${PRIVCAP}-}
done

%install
rm -rf %{buildroot}

install -Ddm 000755 %{buildroot}/etc/yum.repos.d

for FILE in %{MYBUILDIR}/*.repo
do
   install -m 000644 ${FILE} %{buildroot}/etc/yum.repos.d
done


%files
%defattr(000644,root,root,000755)
%doc
%config /etc/yum.repos.d/*



%changelog

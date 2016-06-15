Name: rpm-test
Version: 0.1.0
Release: 1
Summary: Test rpm package
License: BSD
Vendor: typesafe
URL: http://github.com/sbt/sbt-native-packager
AutoProv: yes
AutoReq: yes
BuildRoot: /home/andreas/dev/scriptlets-override-rpm/target/rpm/buildroot
BuildArch: noarch

%description
Description


%install
if [ -e "$RPM_BUILD_ROOT" ]; then
  mv "/home/andreas/dev/scriptlets-override-rpm/target/rpm/tmp-buildroot"/* "$RPM_BUILD_ROOT"
else
  mv "/home/andreas/dev/scriptlets-override-rpm/target/rpm/tmp-buildroot" "$RPM_BUILD_ROOT"
fi

%pre
# #######################################
# ## SBT Native Packager Bash Library  ##
# #######################################

# Adding system user
# $1 = user
# $2 = uid
# $3 = group
# $4 = description
# $5 = shell (defaults to /bin/false)
addUser() {
    user="$1"
    if [ -z "$user" ]; then
	echo "usage: addUser user [group] [description] [shell]"
	exit 1
    fi
    uid="$2"
    if [ -z "$uid" ]; then
	uid_flags=""
	  else
  uid_flags="--uid $uid"
    fi
    group=${3:-$user}
    descr=${4:-No description}
    shell=${5:-/bin/false}
    if ! getent passwd | grep -q "^$user:";
    then
	echo "Creating system user: $user in $group with $descr and shell $shell"
	useradd $uid_flags --gid $group -r --shell $shell -c "$descr" $user
    fi
}

# Adding system group
# $1 = group
# $2 = gid
addGroup() {
    group="$1"
    gid="$2"
    if [ -z "$gid" ]; then
	  gid_flags=""
  else
    gid_flags="--gid $gid"
  fi
    if ! getent group | grep -q "^$group:" ;
    then
	echo "Creating system group: $group"
	groupadd $gid_flags -r $group
    fi
}

# Will return true even if deletion fails
# $1 = user
deleteUser() {
    if hash deluser 2>/dev/null; then
	deluser --quiet --system $1 > /dev/null || true
    elif hash userdel 2>/dev/null; then
	userdel $1
    else
	echo "WARNING: Could not delete user $1 . No suitable program (deluser, userdel) found"
    fi
}

# Will return true even if deletion fails
# $1 = group
deleteGroup() {
    if hash delgroup 2>/dev/null; then
	delgroup --quiet --system $1 > /dev/null || true
    elif hash groupdel 2>/dev/null; then
	groupdel $1
    else
	echo "WARNING: Could not delete user $1 . No suitable program (delgroup, groupdel) found"
    fi
}

# #######################################


# Scriptlet syntax: http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Syntax
# $1 == 1 is first installation and $1 == 2 is upgrade
if [ $1 -eq 1 ] ;
then
    # Adding system user/group : rpm-test and rpm-test

    addGroup rpm-test ""
    addUser rpm-test "" rpm-test "rpm-test user-daemon" "/bin/false"
fi

if [ -e /etc/sysconfig/rpm-test ] ;
then
  sed -i 's/PACKAGE_PREFIX\=.*//g' /etc/sysconfig/rpm-test
fi

if [ -n "$RPM_INSTALL_PREFIX" ] ;
then
  echo "PACKAGE_PREFIX=${RPM_INSTALL_PREFIX}" >> /etc/sysconfig/rpm-test
fi



%post
# POST

## This POST entry will be 2 times in the SPEC file

# POST

## This POST entry will be 2 times in the SPEC file


relocateLink() {
  if [ -n "$4" ] ;
  then
    RELOCATED_INSTALL_DIR="$4/$3"
    echo "${1/$2/$RELOCATED_INSTALL_DIR}"
  else
    echo "$1"
  fi
}
rm -rf $(relocateLink /usr/bin/rpm-test /usr/share/rpm-test rpm-test $RPM_INSTALL_PREFIX) && ln -s $(relocateLink /usr/share/rpm-test/bin/rpm-test /usr/share/rpm-test rpm-test $RPM_INSTALL_PREFIX) $(relocateLink /usr/bin/rpm-test /usr/share/rpm-test rpm-test $RPM_INSTALL_PREFIX)
rm -rf $(relocateLink /usr/share/rpm-test/logs /usr/share/rpm-test rpm-test $RPM_INSTALL_PREFIX) && ln -s $(relocateLink /var/log/rpm-test /usr/share/rpm-test rpm-test $RPM_INSTALL_PREFIX) $(relocateLink /usr/share/rpm-test/logs /usr/share/rpm-test rpm-test $RPM_INSTALL_PREFIX)


%preun
echo preun

echo preun



%postun
echo postun

# POSTUN

## This POSTUN entry will be 2 times in the SPEC file

echo postun

# POSTUN

## This POSTUN entry will be 2 times in the SPEC file


relocateLink() {
  if [ -n "$4" ] ;
  then
    RELOCATED_INSTALL_DIR="$4/$3"
    echo "${1/$2/$RELOCATED_INSTALL_DIR}"
  else
    echo "$1"
  fi
}
[ -e /etc/sysconfig/rpm-test ] && . /etc/sysconfig/rpm-test
rm -rf $(relocateLink /usr/bin/rpm-test /usr/share/rpm-test rpm-test $PACKAGE_PREFIX)
rm -rf $(relocateLink /usr/share/rpm-test/logs /usr/share/rpm-test rpm-test $PACKAGE_PREFIX)


%files
%attr(0755,root,root) /usr/share/rpm-test/bin/rpm-test
%attr(0644,root,root) /usr/share/rpm-test/lib/rpm-test.rpm-test-0.1.0.jar
%attr(0644,root,root) /usr/share/rpm-test/lib/org.scala-lang.scala-library-2.11.8.jar
%dir %attr(755,rpm-test,rpm-test) /var/log/rpm-test
%config %attr(644,root,root) /etc/default/rpm-test
%dir %attr(755,rpm-test,rpm-test) /var/run/rpm-test
%attr(0755,root,root) /etc/init.d/rpm-test

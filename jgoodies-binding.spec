%define oname JGoodies
%define shortoname Binding
%define releasedate 20150121

%define bname %(echo %oname | tr [:upper:] [:lower:])
%define shortname %(echo %shortoname | tr [:upper:] [:lower:])

%define version 2.13.0
%define oversion %(echo %version | tr \. _)

Summary:	Swing Data Binding Framework
Name:		%{bname}-%{shortname}
Version:	%{version}
Release:	1
License:	BSD
Group:		Development/Java
URL:		http://www.jgoodies.com/freeware/libraries/%{shortname}/
Source0:	http://www.jgoodies.com/download/libraries/%{shortname}/%{name}-%{oversion}-%{releasedate}.zip
# NOTE: Latest version of jgoodies libraries can't be freely download from
#	from the official site. However official maven repo provides some
#	more updated versions
# Source0:	https://repo1.maven.org/maven2/com/%{bname}/%{name}/%{version}/%{name}-%{version}-sources.jar
BuildArch:	noarch

BuildRequires:	java-rpmbuild
BuildRequires:	maven-local
BuildRequires:	mvn(com.jgoodies:jgoodies-common) >= 1.8
# The following are required for tests only
BuildRequires:	x11-server-xvfb
BuildRequires:	mvn(junit:junit)

Requires:	java-headless >= 1.6
Requires:	jpackage-utils
Requires:	mvn(com.jgoodies:jgoodies-common) >= 1.8

%description
The JGoodies Binding synchronizes object properties with Swing components.
And it helps you represent the state and behavior of a presentation
independently of the GUI components used in the interface.

The JGoodies Binding requires Java 6 or later.

%files -f .mfiles
%doc README.html
%doc RELEASE-NOTES.txt
%doc LICENSE.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{oname} %{shortoname}
Requires:	jpackage-utils

%description javadoc
API documentation for %{oname} %{shortoname}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q
# Extract sources
mkdir -p src/main/java/
pushd src/main/java/
%jar -xf ../../../%{name}-%{version}-sources.jar
popd

# Extract tests
mkdir -p src/test/java/
pushd src/test/java/
%jar -xf ../../../%{name}-%{version}-tests.jar
popd

# Delete prebuild JARs and binaries and docs
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm -fr docs

# Add the META-INF/INDEX.LIST to the jar archive (fix jar-not-indexed warning)
%pom_add_plugin :maven-jar-plugin . "<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
xvfb-run -a %mvn_build

%install
%mvn_install


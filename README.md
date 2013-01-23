mozdeploy
=========

Build
=====
inputs: app, build_dir, version (usually git ref)

Steps
-----
* Generates build_id $timestamp-$version (truncated to 31 characters)
* Calls application build script and passes in (version, build_id, build_dir)
* Application build script builds a complete release in $build_dir/$build_id
    * Example: a application with virtualenv might look like $build_dir/$build_id/$app_name and $build_dir/$build_id/venv
    * The application may drop a executable install script @ $build_dir/$build_id/.postinstall which will be run after successfully unpacking
* Create package (tarball/rpm) which includes ./$build_id/* and move the package to our http server at http(s)://$pkgserver/$pkgroot/$app/$build_id/release.tar
   * $pkgroot might be something like addons-dev or addons-stage
* Write $build_id to $app/LATEST


Deploy
======
A package host and root will be defined in the script or a config file
inputs: app_dir, app, build_id

Steps:
* if $build_id is LATEST, fetch $pkgserver/$app/LATEST and set $build_id to that value
* If $app_dir/$build_id does not exist then:
   * Fetch package from $pkgserver/$app/$build_id/release.tar
   * Unpack in to $app_dir/
* Symlink $app_dir/current to $app_dir/$build_id
* cd $app_dir/$build_id; run ./.postinstall


Notes
======
This service should be able to use server signed client certificates to auth with the packagehost.

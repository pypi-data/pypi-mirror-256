A command and utility functions for making listings of file content hashcodes
and manipulating directory trees based on such a hash index.

*Latest release 20240211.1*:
Better module docstring.

## Function `dir_filepaths(dirpath: str)`

Generator yielding the filesystem paths of the files in `dirpath`.

## Function `dir_remap(srcdirpath: str, fspaths_by_hashcode: Mapping[cs.hashutils.BaseHashCode, List[str]], *, hashname: str)`

Generator yielding `(srcpath,[remapped_paths])` 2-tuples
based on the hashcodes keying `rfspaths_by_hashcode`.

## Function `file_checksum(fspath: str, hashname: str = 'sha256', *, fstags: cs.fstags.FSTags) -> Optional[cs.hashutils.BaseHashCode]`

Return the hashcode for the contents of the file at `fspath`.
Warn and return `None` on `OSError`.

## Function `get_fstags_hashcode(fspath: str, hashname: str, fstags: cs.fstags.FSTags) -> Tuple[Optional[cs.hashutils.BaseHashCode], Optional[os.stat_result]]`

Obtain the hashcode cached in the fstags if still valid.
Return a 2-tuple of `(hashcode,stat_result)`
where `hashcode` is a `BaseHashCode` subclass instance is valid
or `None` if missing or no longer valid
and `stat_result` is the current `os.stat` result for `fspath`.

## Function `hashindex(fspath, *, hashname: str, fstags: cs.fstags.FSTags)`

Generator yielding `(hashcode,filepath)` 2-tuples
for the files in `fspath`, which may be a file or directory path.
Note that it yields `(None,filepath)` for files which cannot be accessed.

## Class `HashIndexCommand(cs.cmdutils.BaseCommand)`

Tool to generate indices of file content hashcodes
and to link files to destinations based on their hashcode.

Command line usage:

    Usage: hashindex subcommand...
        Generate or process file content hash listings.
      Subcommands:
        help [-l] [subcommand-names...]
          Print help for subcommands.
          This outputs the full help for the named subcommands,
          or the short help for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        linkto [-f] [-h hashname] [--mv] [-n] [-q] [-s] srcdir dstdir < hashindex
          Link files from srcdir to dstdir according the input hash index.
          -f    Force: link even if the target already exists.
          -h hashname
                Specify the hash algorithm, default: sha256
          --mv  Move: unlink the original after a successful hard link.
          -n    No action; recite planned actions.
          -q    Quiet. Do not report actions.
          -s    Symlink the source file instead of hard linking.
        ls [-h hashname] [-r] paths...
          Walk the filesystem paths and emit a listing.
          -h hahsname   Specify the file content hash alogrith name.
          -r            Emit relative paths in the listing.
                        This requires each path to be a directory.
        rearrange [options...] {[[user@]host:]refdir|-} [[user@]rhost:]targetdir
          Rearrange files in targetdir based on their positions in refdir.
          Options:
            -e ssh_exe  Specify the ssh executable.
            -h hashname Specify the file content hash algorithm name.
            -H hashindex_exe
                        Specify the remote hashindex executable.
            --mv        Move mode.
            -n          No action, dry run.
            -s          Symlink mode.
        shell
          Run a command prompt via cmd.Cmd using this command's subcommands.

*`HashIndexCommand.Options`*

*Method `HashIndexCommand.cmd_linkto(self, argv, *, fstags: cs.fstags.FSTags)`*:
Usage: {cmd} [-f] [-h hashname] [--mv] [-n] [-q] [-s] srcdir dstdir < hashindex
Link files from srcdir to dstdir according the input hash index.
-f    Force: link even if the target already exists.
-h hashname
      Specify the hash algorithm, default: {DEFAULT_HASHNAME}
--mv  Move: unlink the original after a successful hard link.
-n    No action; recite planned actions.
-q    Quiet. Do not report actions.
-s    Symlink the source file instead of hard linking.

*Method `HashIndexCommand.cmd_ls(self, argv)`*:
Usage: {cmd} [-h hashname] [-r] paths...
Walk the filesystem paths and emit a listing.
-h hahsname   Specify the file content hash alogrith name.
-r            Emit relative paths in the listing.
              This requires each path to be a directory.

*Method `HashIndexCommand.cmd_rearrange(self, argv)`*:
Usage: {cmd} [options...] {{[[user@]host:]refdir|-}} [[user@]rhost:]targetdir
Rearrange files in targetdir based on their positions in refdir.
Options:
  -e ssh_exe  Specify the ssh executable.
  -h hashname Specify the file content hash algorithm name.
  -H hashindex_exe
              Specify the remote hashindex executable.
  --mv        Move mode.
  -n          No action, dry run.
  -s          Symlink mode.

## Function `main(argv=None)`

Commandline implementation.

## Function `merge(srcpath: str, dstpath: str, *, opname=None, hashname: str, move_mode: bool = False, symlink_mode=False, doit=False, quiet=False, fstags: cs.fstags.FSTags)`

Merge `srcpath` to `dstpath`.

If `dstpath` does not exist, move/link/symlink `srcpath` to `dstpath`.
Otherwise checksum their contents and raise `FileExistsError` if they differ.

## Function `paths_remap(srcpaths: Iterable[str], fspaths_by_hashcode: Mapping[cs.hashutils.BaseHashCode, List[str]], *, hashname: str)`

Generator yielding `(srcpath,fspaths)` 2-tuples.

## Function `read_hashindex(f, start=1, *, hashname: str)`

A generator which reads line from the file `f`
and yields `(hashcode,fspath)` 2-tuples.
If there are parse errors the `hashcode` or `fspath` may be `None`.

## Function `rearrange(srcdirpath: str, rfspaths_by_hashcode, *, hashname: str, move_mode: bool = False, symlink_mode=False, doit: bool, quiet: bool = False, fstags: cs.fstags.FSTags, runstate: cs.resources.RunState)`

Rearrange the files in `dirpath` according to the
hashcode->[relpaths] `fspaths_by_hashcode`.

## Function `set_fstags_hashcode(fspath: str, hashcode, S: os.stat_result, fstags: cs.fstags.FSTags)`

Record `hashcode` against `fspath`.

# Release Log



*Release 20240211.1*:
Better module docstring.

*Release 20240211*:
Initial PyPI release: "hashindex" command and utility functions for listing file hashcodes and rearranging trees based on a hash index.

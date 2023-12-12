#!/usr/bin/env python
"""Script used by the `remap_user.yml` task to remap users and groups.

Given a list of existing user or group ids and desired user or group ids,
compute a mapping from existing user or group ids to new user or group ids that
do not conflict with other existing ids nor the desired ids.

For example, assume service "fwupd" has created a user named "fwupd" and the
operating system has assigned UID 999 to it. Furthermore, assume that two new
applications need to run on the server (for example, Galaxy and HTCondor) with
UIDs 999 and 3 respectively (for example, because they need to access a remote
filesystem using NFS and the server has already allocated UIDs 999 and 3 to the
applications, meaning that existing files belonging to the applications are
already owned by UIDs 999 and 3 respectively). In addition, assume the
/etc/passwd file looks as follows:

```
root:x:0:0::/root:/bin/bash
bin:x:1:1::/:/usr/bin/nologin
daemon:x:2:2::/:/usr/bin/nologin
mail:x:8:12::/var/spool/mail:/usr/bin/nologin
fwupd:x:999:962:Firmware update daemon:/var/lib/fwupd:/usr/bin/nologin
```

It is then necessary to remap the "fwupd" user to a different UID so that 999
becomes free for the first application (e.g. Galaxy). This script can find a
new UID for "fwupd" that is different both from 999 and 3. To do so, call it
passing as arguments the existing and desired UIDs as demonstrated below.

```
./remap_user.py \
  -e 0:root \
  -e 1:bin \
  -e 2:daemon \
  -e 8:mail \
  -d 999:galaxy \
  -d 3:condor
```

The output of the call is shown below. Notice that user 999 ("fwupd") does not
get mapped to UID 3, despite it being free, since it is meant to belong to user
"condor".

```
EXISTING    TARGET
     999         4
```
"""

from argparse import ArgumentParser
from os.path import basename, splitext
from sys import stdout
from typing import Iterator, Mapping


def ordered_complement(integers: set[int]) -> Iterator[int]:
    """Yield from the complement of a set of nonnegative integers.

    Yield from the complement of a set of nonnegative integers in ascending
    order.

    Args:
        integers: Set of nonnegative integers to yield the complement of.

    Yields:
        Nonnegative integers from the complement of the set passed as input, in
        ascending order.
    """
    i = 0
    while True:
        if i not in integers:
            yield i
        i += 1


def resolve_conflicts(
    mapping_existing: Mapping[int, str], mapping_desired: Mapping[int, str]
) -> Mapping[int, int]:
    """Resolve conflicts between existing and desired user or group ids.

    Given a mapping defining the existing group or user ids and desired user or
    group ids, compute a mapping from existing group or user ids to new ids
    that do not conflict with other existing ids nor the desired ids.

    Args:
        mapping_existing: Already defined user or group ids.
        mapping_desired: Desired arrangement of user or group ids
            (non-exhaustive).

    Returns:
        Mapping from existing user or group ids to new user or group ids that
        resolves the conflicts between existing and desired ids.
    """
    conflicts = {
        id_
        for id_ in mapping_existing.keys() & mapping_desired.keys()
        if mapping_existing[id_] != mapping_desired[id_]
    }
    resolution = {
        id_existing: id_target
        for id_existing, id_target in zip(
            conflicts,
            ordered_complement(
                mapping_existing.keys() | mapping_desired.keys()
            ),
        )
    }
    return resolution


def make_parser() -> ArgumentParser:
    """Command line interface for this script."""
    parser = ArgumentParser(
        prog=splitext(basename(__file__))[0],
        description="Remap user or group ids",
    )

    def convert_argument(string: str) -> tuple[int, str]:
        """Convert a user or group id in the form "ID:NAME" to a tuple."""
        id_, name = string.split(":")
        id_ = int(id_)
        return id_, name

    parser.add_argument(
        "-e",
        "--existing",
        dest="existing",
        metavar="ID:NAME",
        action="extend",
        default=[],
        nargs="+",
        required=True,
        type=convert_argument,
        help="existing user/group id and name (separated by a colon)",
    )
    parser.add_argument(
        "-d",
        "--desired",
        dest="desired",
        metavar="ID:NAME",
        action="extend",
        default=[],
        nargs="+",
        required=True,
        type=convert_argument,
        help="desired user/group id and name (separated by a colon)",
    )

    return parser


if __name__ == "__main__":
    command_parser = make_parser()
    command_args = command_parser.parse_args()

    existing = {id_: name for id_, name in command_args.existing}
    desired = {id_: name for id_, name in command_args.desired}
    mapping = resolve_conflicts(existing, desired)

    col_length = max(
        len(str(x))
        for x in ("EXISTING", "TARGET", *mapping.keys(), *mapping.values())
    )
    row_fmt = "\t".join((f"{{:>{col_length}}}",) * 2)
    if mapping:
        print(row_fmt.format("EXISTING", "TARGET"), file=stdout)
        for existing_id, target_id in mapping.items():
            print(row_fmt.format(existing_id, target_id), file=stdout)

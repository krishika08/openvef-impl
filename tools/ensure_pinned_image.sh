#!/usr/bin/env bash
# D-028 recurrence guard: before every evidence run, the image tag must resolve to the pinned
# image ID (tools/pinned-image.conf). If it does not (tag absent, or pointing at another image),
# the image is loaded from the saved tarball, after its size and SHA-256 are checked, and the ID
# is checked again. The guard never builds an image: a rebuild gives a different image ID
# (docs/ENV-CHANGE-2026-11-27.md). Exit 0 only when the tag resolves to the pinned ID.
# Usage: tools/ensure_pinned_image.sh <tag>. Prints one status line on stdout:
#   IMAGE_GUARD OK <id>  |  IMAGE_GUARD RESTORED_FROM_TARBALL <was> -> <id> (<tarball sha256>)
set -euo pipefail
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CONF="$REPO/tools/pinned-image.conf"
val() { sed -n "s/^$1=\(.*\)$/\1/p" "$CONF"; }
PIN_TAG=$(val PINNED_IMAGE_TAG); PIN_ID=$(val PINNED_IMAGE_ID)
TARBALL=$(val PINNED_TARBALL); TAR_SHA=$(val PINNED_TARBALL_SHA256); TAR_BYTES=$(val PINNED_TARBALL_BYTES)
fail() { echo "image guard: $*" >&2; exit 3; }
TAG=${1:?usage: ensure_pinned_image.sh <tag>}
[ "$TAG" = "$PIN_TAG" ] || fail "tag $TAG is not the pinned tag $PIN_TAG (Dockerfile or lock changed?); an owner decision must update tools/pinned-image.conf"
current() { docker image inspect "$TAG" --format '{{.Id}}' 2>/dev/null || true; }
was=$(current)
if [ "$was" = "$PIN_ID" ]; then echo "IMAGE_GUARD OK $PIN_ID"; exit 0; fi
echo "image guard: $TAG resolves to '${was:-<absent>}', expected $PIN_ID; loading $TARBALL" >&2
[ -f "$TARBALL" ] || fail "tarball $TARBALL is missing"
[ "$(stat -c %s "$TARBALL")" = "$TAR_BYTES" ] || fail "tarball size differs from $TAR_BYTES"
[ "$(sha256sum "$TARBALL" | cut -c1-64)" = "$TAR_SHA" ] || fail "tarball SHA-256 differs from $TAR_SHA"
docker load -q -i "$TARBALL" >&2
now=$(current)
[ "$now" = "$PIN_ID" ] || fail "after loading, $TAG resolves to '${now:-<absent>}', expected $PIN_ID"
echo "IMAGE_GUARD RESTORED_FROM_TARBALL ${was:-<absent>} -> $PIN_ID ($TAR_SHA)"

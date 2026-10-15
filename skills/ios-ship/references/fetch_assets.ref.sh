#!/usr/bin/env bash
# Example (from a real game build) — pull the live web bundle into www/ and vendor
# the render libs. The asset mirror is the single source of truth for the app; this
# script snapshots it
# into the app binary (offline core game; live rails still reach the network).
set -euo pipefail
BASE="${ASSET_BASE_URL:?set ASSET_BASE_URL to your bundle mirror, e.g. https://pub-XXXX.r2.dev/yourapp}"
THREE="https://cdn.jsdelivr.net/npm/three@0.160.0"
mkdir -p www
grab(){ mkdir -p "www/$(dirname "$1")"; curl -fsSL --retry 3 -o "www/$1" "$BASE/$1"; echo "  $1"; }
vend(){ mkdir -p "www/vendor/$(dirname "$1")"; curl -fsSL --retry 3 -o "www/vendor/$1" "$THREE/$2"; echo "  vendor/$1"; }

echo "== app art (icon + splash sources) =="
mkdir -p assets
for a in icon-only.png splash.png splash-dark.png; do
  curl -fsSL --retry 3 -o "assets/$a" "$BASE/appicons/$a"; echo "  assets/$a"
done

echo "== app bundle =="
grab "index.html"
# …list every file your bundle ships, e.g.:
# grab "app.js"
# grab "data/courses.json"
# grab "models/<model>.gltf"

echo "== vendored render stack (offline + review-safe) =="
vend "three.module.js"                     "build/three.module.js"
vend "jsm/loaders/GLTFLoader.js"           "examples/jsm/loaders/GLTFLoader.js"
vend "jsm/loaders/DRACOLoader.js"          "examples/jsm/loaders/DRACOLoader.js"
vend "jsm/loaders/KTX2Loader.js"           "examples/jsm/loaders/KTX2Loader.js"
vend "jsm/utils/BufferGeometryUtils.js"    "examples/jsm/utils/BufferGeometryUtils.js"
vend "jsm/utils/WorkerPool.js"             "examples/jsm/utils/WorkerPool.js"
vend "jsm/libs/ktx-parse.module.js"        "examples/jsm/libs/ktx-parse.module.js"
vend "jsm/libs/zstddec.module.js"          "examples/jsm/libs/zstddec.module.js"
vend "jsm/libs/draco/gltf/draco_decoder.js"      "examples/jsm/libs/draco/gltf/draco_decoder.js"
vend "jsm/libs/draco/gltf/draco_decoder.wasm"    "examples/jsm/libs/draco/gltf/draco_decoder.wasm"
vend "jsm/libs/draco/gltf/draco_wasm_wrapper.js" "examples/jsm/libs/draco/gltf/draco_wasm_wrapper.js"
vend "jsm/libs/basis/basis_transcoder.js"        "examples/jsm/libs/basis/basis_transcoder.js"
vend "jsm/libs/basis/basis_transcoder.wasm"      "examples/jsm/libs/basis/basis_transcoder.wasm"

echo "== rewire the app copy to the vendored stack =="
# Handle EVERY vendor-path family the web build has ever used (CDN and the
# asset mirror). Absolute paths cannot resolve inside the app bundle.
sed -i.bak \
  -e 's#https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js#./vendor/three.module.js#g' \
  -e 's#https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/#./vendor/jsm/#g' \
  -e 's#/mirror/vendor/three/build/three.module.js#./vendor/three.module.js#g' \
  -e 's#/mirror/vendor/three/examples/jsm/#./vendor/jsm/#g' \
  -e 's#/mirror/vendor/draco/#./vendor/jsm/libs/draco/gltf/#g' \
  www/index.html && rm -f www/index.html.bak

echo "== sanity =="
test -s www/index.html && test -s www/sim.js && test -s www/packs/olive_drive.json
grep -q '"three": *"./vendor/three.module.js"' www/index.html || grep -q '"three":"./vendor/three.module.js"' www/index.html || { echo "importmap not vendored!"; exit 1; }
! grep -q "cdn.jsdelivr.net" www/index.html || { echo "CDN refs remain!"; exit 1; }
! grep -q "/mirror/" www/index.html || { echo "mirror absolute refs remain!"; exit 1; }
echo "bundle OK: $(du -sh www | cut -f1)"

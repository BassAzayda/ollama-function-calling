#!/usr/bin/env bash
# Wipe and reinstall a corrupted Wan2GP checkout, clearing stale bytecode/caches.
#
# Defaults are conservative: your generated outputs, settings and downloaded
# model weights (ckpts/, loras*/) are moved aside and restored into the fresh
# clone. Nothing is deleted until the new clone succeeds.
#
# Usage:
#   ./reinstall_wan2gp.sh                 # keep models + outputs, fresh code
#   ./reinstall_wan2gp.sh --purge-models  # also drop ckpts/ and loras/ (re-download)
#   ./reinstall_wan2gp.sh --purge-hf      # also clear ~/.cache/huggingface (BIG re-download)
#   WAN_DIR=/data/Wan2GP ./reinstall_wan2gp.sh
set -euo pipefail

WAN_DIR="${WAN_DIR:-$HOME/Wan2GP}"
REPO="${WAN_REPO:-https://github.com/deepbeepmeep/Wan2GP.git}"
PY="${PYTHON:-python3}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="${WAN_DIR}.broken-${STAMP}"
STASH="$(mktemp -d "${TMPDIR:-/tmp}/wan2gp-keep-XXXXXX")"

PURGE_MODELS=0
PURGE_HF=0
for arg in "$@"; do
  case "$arg" in
    --purge-models) PURGE_MODELS=1 ;;
    --purge-hf)     PURGE_HF=1 ;;
    -h|--help)      sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

say() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }

# Data worth carrying across the reinstall. ckpts/loras are only kept when
# --purge-models is NOT set; they are typically tens of GB.
KEEP=(outputs settings.json wgp_config.json .env)
if [ "$PURGE_MODELS" -eq 0 ]; then
  KEEP+=(ckpts loras loras_i2v loras_hunyuan loras_ltxv loras_flux)
fi

if [ -d "$WAN_DIR" ]; then
  say "Stashing user data from $WAN_DIR"
  for item in "${KEEP[@]}"; do
    if [ -e "$WAN_DIR/$item" ]; then
      echo "  keep: $item"
      mv "$WAN_DIR/$item" "$STASH/"
    fi
  done

  say "Moving corrupted checkout to $BACKUP"
  mv "$WAN_DIR" "$BACKUP"
else
  echo "No existing $WAN_DIR — doing a clean install."
fi

say "Cloning fresh copy of Wan2GP"
git clone "$REPO" "$WAN_DIR"

say "Restoring kept data"
shopt -s dotglob nullglob
for item in "$STASH"/*; do
  echo "  restore: $(basename "$item")"
  mv "$item" "$WAN_DIR/"
done
shopt -u dotglob nullglob
rmdir "$STASH" 2>/dev/null || true

say "Clearing stale Python bytecode in $WAN_DIR"
find "$WAN_DIR" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$WAN_DIR" \( -name '*.pyc' -o -name '*.pyo' \) -delete 2>/dev/null || true

say "Clearing pip download/wheel cache"
"$PY" -m pip cache purge >/dev/null 2>&1 || true

if [ "$PURGE_HF" -eq 1 ]; then
  say "Clearing HuggingFace hub cache (this forces a full re-download)"
  rm -rf "${HF_HOME:-$HOME/.cache/huggingface}"
fi

say "Creating a fresh virtualenv at $WAN_DIR/venv"
rm -rf "$WAN_DIR/venv"
"$PY" -m venv "$WAN_DIR/venv"
# shellcheck disable=SC1091
source "$WAN_DIR/venv/bin/activate"

say "Installing PyTorch (CUDA 12.4 build)"
python -m pip install --upgrade pip wheel
python -m pip install --no-cache-dir \
  torch==2.6.0 torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/test/cu124

say "Installing Wan2GP requirements"
python -m pip install --no-cache-dir -r "$WAN_DIR/requirements.txt"

say "Done"
cat <<EOF

Fresh install at: $WAN_DIR
Old (corrupted)  : ${BACKUP:-<none>}

Verify it runs, then delete the backup yourself:
    rm -rf "$BACKUP"

To start:
    cd "$WAN_DIR" && source venv/bin/activate && python wgp.py
EOF

#!/usr/bin/env bash
set -euo pipefail

for name in API_DEPLOY_HOOK WEB_DEPLOY_HOOK API_URL WEB_URL GITHUB_SHA; do
  if [ -z "${!name:-}" ]; then
    echo "::error::Falta configurar $name. No se acreditó despliegue."
    exit 1
  fi
done

for hook in "$API_DEPLOY_HOOK" "$WEB_DEPLOY_HOOK"; do
  separator='?'
  if [[ "$hook" == *'?'* ]]; then separator='&'; fi
  curl --fail --silent --show-error --request POST \
    "${hook}${separator}ref=${GITHUB_SHA}" --output /dev/null
done

for attempt in $(seq 1 40); do
  if curl --fail --silent --connect-timeout 10 --max-time 20 "$API_URL/ready" |
    jq --exit-status --arg sha "$GITHUB_SHA" '.commit == $sha' >/dev/null &&
    curl --fail --silent --connect-timeout 10 --max-time 20 "$WEB_URL/version.json" |
    jq --exit-status --arg sha "$GITHUB_SHA" '.commit == $sha' >/dev/null; then
    echo "API y web disponibles con el commit esperado."
    exit 0
  fi
  echo "Esperando el commit verificado: intento $attempt/40"
  sleep 15
done
echo '::error::No se verificó el commit esperado en ambos servicios.'
exit 1

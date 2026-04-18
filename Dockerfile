# =============================================================================
# CTS Tool Skeleton — Dockerfile
# =============================================================================
#
# OPTION A: Wrap an existing public image (preferred when one exists)
#
#   FROM public-registry/tool-name:version
#   ENTRYPOINT ["tool-command"]
#
# OPTION B: Build from scratch
#
#   FROM ubuntu:24.04 AS build
#   RUN apt-get update && apt-get install -y wget
#   RUN wget https://example.com/tool-v1.0.tar.gz && tar xzf tool-v1.0.tar.gz
#
#   FROM ubuntu:24.04
#   COPY --from=build /tool /usr/local/bin/tool
#   ENTRYPOINT ["tool"]
#
# CTS CONTAINER REQUIREMENTS:
#   - Must be publicly accessible (no auth)
#   - Must run as non-root
#   - Must have /bin/bash
#   - Must define ENTRYPOINT
#   - Must write ALL output to the output_mount_point only (/out by default)
#   - Must NOT download external files at runtime
#   - Must NOT hardlink between input and output directories
#
# =============================================================================

FROM replaceme/tool:version

ENTRYPOINT ["tool-command"]

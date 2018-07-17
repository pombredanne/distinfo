ifdef IN_NIX_SHELL

SHELL = bash -eu -o pipefail

override MAKEFLAGS += --no-builtin-rules --warn-undefined-variables

.DELETE_ON_ERROR:

ARGS ?=

.PHONY: test
test:
	pytest $(ARGS)

.PHONY: lint
lint:
	prospector --with-tool=mccabe --with-tool=pyroma --with-tool=vulture $(ARGS)

.PHONY: todo
todo:
	git grep --line-number "FIXME|HACK|TODO|TOGO"

.PHONY: clean
clean:
	git clean -fdX

endif

ifdef TRAVIS

define NIX_CONF
cores = $(shell nproc)
substituters = https://cache.nixos.org https://cachix.cachix.org https://distinfo.cachix.org
trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY= cachix.cachix.org-1:eWNHQldwUO7G2VkjpnjDbWwy4KQ/HNxht7H4SSoMckM= distinfo.cachix.org-1:nj8IiFYM7vGOYIvh/KZW/DJ7VezbcNep0R4cPNr6lls=
endef
export NIX_CONF

.PHONY: travis-setup
travis-setup:
	mkdir -p /etc/nix
	echo "$$NIX_CONF" > /etc/nix/nix.conf

.PHONY: travis-run
travis-run: PATH := $(HOME)/.local/bin:$(PATH)
travis-run:
	nix-env --install --file https://github.com/cachix/cachix/tarball/master
	nix-build --show-trace
	cachix push distinfo result
	cd result && bin/codecov

endif

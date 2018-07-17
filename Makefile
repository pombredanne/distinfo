SHELL = bash -eu -o pipefail

override MAKEFLAGS += --no-builtin-rules --warn-undefined-variables

.DELETE_ON_ERROR:

ARGS ?=

.PHONY: result
result:
	nix-build --show-trace

.PHONY: push
push: result
	cachix push distinfo $<

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

ifdef TRAVIS

define NIX_CONF
cores = $(shell nproc)
max-jobs = $(shell nproc)
sandbox = true
substituters = https://cache.nixos.org https://cachix.cachix.org https://distinfo.cachix.org
trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY= cachix.cachix.org-1:eWNHQldwUO7G2VkjpnjDbWwy4KQ/HNxht7H4SSoMckM= distinfo.cachix.org-1:nj8IiFYM7vGOYIvh/KZW/DJ7VezbcNep0R4cPNr6lls=
endef
export NIX_CONF

cc-test-reporter:
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > $@
	chmod +x $@
	./$@ before-build

.PHONY: travis-setup
travis-setup: cc-test-reporter
	sudo mkdir -p /etc/nix
	echo "$$NIX_CONF" | sudo tee /etc/nix/nix.conf
	nix-env --install --file https://github.com/cachix/cachix/tarball/v0.1.0.2

.PHONY: travis-reports
travis-reports:
	ls -l result/
	./cc-test-reporter after-build --prefix ./result --coverage-input-type coverage.py

endif

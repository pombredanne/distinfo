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

.PHONY: ci
ci: test
	codeclimate-test-reporter
	codecov

.PHONY: clean
clean:
	git clean -fdX

endif

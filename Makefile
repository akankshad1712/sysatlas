
CC ?= cc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Wpedantic -Wconversion -Werror
BUILD := build

.PHONY: all test test-c test-python sanitize clean run

all: $(BUILD)/sysatlas-collector

$(BUILD)/sysatlas-collector: collector/src/collector.c
	mkdir -p $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

test-c: all
	bash ./collector/tests/test_collector.sh ./$(BUILD)/sysatlas-collector

test-python:
	python -m pytest -q

test: test-c test-python

sanitize:
	mkdir -p $(BUILD)
	$(CC) -std=c11 -g -O1 -Wall -Wextra -Wpedantic -fsanitize=address,undefined -fno-omit-frame-pointer collector/src/collector.c -o $(BUILD)/sysatlas-collector-sanitize
	bash ./collector/tests/test_collector.sh ./$(BUILD)/sysatlas-collector-sanitize

run: all
	uvicorn app.main:app --host 127.0.0.1 --port 8000

clean:
	rm -rf $(BUILD) .pytest_cache data

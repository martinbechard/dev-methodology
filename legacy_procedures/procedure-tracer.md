# Tracer Utility Guide

This guide explains how to use the Tracer utility for debugging and tracing execution flow in the CIBC Driver extension.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Core Features](#core-features)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Best Practices](#best-practices)

## Overview

The Tracer is a utility that logs function calls, execution flow, and messages to help with debugging complex logic. It provides hierarchical tracing with proper indentation to visualize the call stack and execution context.

Located in `src/utils/tracer.ts`, this utility makes debugging simpler by providing detailed execution logs with minimal changes to your code.

## Core Features

- **Function Entry/Exit Tracing**: Track when functions are called and when they return
- **Hierarchical Logging**: Visualize call stacks through proper indentation
- **Parameter and Return Value Logging**: See what goes in and what comes out of functions
- **Circular Reference Handling**: Safely log objects with circular references
- **Storage-Based Logging**: All trace output goes to Chrome storage
- **Filtering**: Filter trace output using regular expressions
- **Execution Wrapping**: Easily wrap functions to add tracing
- **Infinite Loop Protection**: Prevents excessive log file growth during testing

## Usage Examples

### Basic Logging

```typescript
import { Tracer } from "./utils/tracer";

// Simple log message
Tracer.log("Processing item", itemId);

// Log with multiple values
Tracer.log("User data:", userId, userData);
```

### Tracing Function Execution

```typescript
import { Tracer, exec } from "./utils/tracer";

// Method 1: Using exec helper
function addNumbers(a: number, b: number): number {
  return a + b;
}
const result = exec(addNumbers, [5, 3]); // Logs entry, execution, and exit

// Method 2: Manual tracing
function processData(data: any, counter: number) {
  Tracer.logEntry("processData", data, counter);

  // Your processing logic here
  const result = transform(data);

  Tracer.logExit("processData", result);
  return result;
}
```

### Wrapping Functions for Tracing

```typescript
import { wrapTracer } from "./utils/tracer";

class DataProcessor {
  private originalProcess(data: any) {
    // Processing logic
    return transformedData;
  }

  // Create a traced version of the function - the entry and exit of
  // the function will be automatically logged
  process = wrapTracer("DataProcessor.process", this.originalProcess, this);
}
```

## API Reference

### Class: `Tracer`

A static class providing tracing functionality.

#### Static Properties

- `maxTraceLevel: number` - Maximum nesting level to trace (default: 0, -1 for unlimited)
- `regexFilters: RegExp | RegExp[] | undefined` - Filters for trace messages
- `maxWrites: number` - Maximum number of lines to write (1000 for testing to prevent infinite loops, -1 for production)

#### Static Methods

- `log(...values: any[]): void` - Logs values to the trace file
- `logEntry(functionName: string, ...values: any[]): void` - Logs a function entry
- `logExit(functionName: string, returnValue?: any): void` - Logs a function exit
- `exec<F, T>(func: F, param: T): ReturnType<F>` - Executes a function with tracing
- `clearLogFile(): void` - Clears the trace log file
- `reset(): void` - Resets the tracer state
- `stringify(value: any): string` - Safely stringifies values

### Helper Functions

- `exec<F, T>(func: F, param: T): ReturnType<F>` - Shorthand for `Tracer.exec`
- `wrapTracer<T>(functionName: string, actualFunction: T, instance?: object): T` - Creates a traced version of a function
- `deepCopy(obj: any, seen?: Set<any>): any` - Creates a deep copy of an object, handling circular references

## Best Practices

1. **Configure Trace Levels Appropriately**:
   ```typescript
   // For focused debugging of a specific module
   Tracer.maxTraceLevel = -1; // Unlimited tracing

   // For normal operation
   Tracer.maxTraceLevel = 0; // Disable tracing
   ```

2. **Use Regex Filters for Focus**:
   ```typescript
   // Only trace messages related to parsing
   Tracer.regexFilters = /parsing|parse/i;

   // Multiple filters
   Tracer.regexFilters = [/error/i, /warning/i];
   ```

3. **Clear the Log File Before Starting a Debugging Session**:
   ```typescript
   Tracer.clearLogFile();
   // This happens automatically when process.env.TRACE_TEST is true
   ```

4. **Prefix Your Log Messages for Easier Filtering**:
   ```typescript
   Tracer.log("RULE: 1.2:", "Found heading:", heading);
   ```

5. **Reset State Between Test Runs**:
   ```typescript
   beforeEach(() => {
     Tracer.reset();
   });
   ```

7. **Respect Write Limits for Testing**:
   ```typescript
   // For testing, the limit is 1000 lines by default to prevent infinite loops
8. // We reset this limit before each test by calling Tracer.reset()
   // In production, this limit is disabled (-1)
   // Do not change this value unless you know what you're doing
   ```

## Example Trace Output

Below is an example of trace output from a typical tracing session:

```
>>> Call TEST it should parse a single section with heading
| RULE: 1: Parsing markdown text : markdownText= # Section 1

This is some text.
| RULE: 1.2: Found heading : heading= Section 1
| RULE: 1.2.1: Set heading level : headingLevel= 1
| RULE: 1.2.3: Set heading and numbering : heading= Section 1  numbering= undefined
| RULE: 2: Processing line : line=
| RULE: 2.3: Added line to text : text=
| RULE: 2: Processing line : line= This is some text.
| RULE: 2.3: Added line to text : text= This is some text.
| RULE: 3: Set text on section : section.text= This is some text.
| RULE: 4: Returning section : section= {"heading":"Section 1","headingLevel":1,"text":"This is some text."}
<<< Exit TEST it should parse a single section with heading
```

In this example:
- `>>> Call TEST...` shows the entry into a test function
- `| RULE: ...` lines show each step in the execution with consistent formatting
- The indentation reflects the call hierarchy
- `<<< Exit TEST...` shows the exit from the function with any return values

By following the trace, you can understand the execution flow and identify issues in complex logic.

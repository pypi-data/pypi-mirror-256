# py\_code\_timing

This package provides a comprehensive range of Python code timing utilities.

## Features and usage


### `CodeTiming`, `start` and `elapsed`

The class `CodeTiming` provides the basic timing functionality, operating rather like a stopwatch.  The basic pattern of use goes like this:

```
    tobj = CodeTiming()
    ...
    tobj.start()
    ...
    cur_time = tobj.elapsed()
    ...
    tobj.start()
    ...
    cur_time = tobj.elapsed()
    ...
```

The call to `start` begins the timing process.   The code between `start` and `elapsed` is timed, with the measured duration returned from the `elapsed` call. Timing stops with the call to `elapsed`, and only resumes when `start` is called again, etc.

### `sample`
Additionally, it can be useful to capture intermediate timings in between `start` and `elapsed`.  This can be done using a call to `sample`, as in this example:

```
    tobj = CodeTiming()
    ...
    tobj.start()
    ...
    cur_time1 = tobj.sample()
    ...
    cur_time2 = tobj.sample()
    ...
    cur_time = tobj.elapsed()
```
As for `elapsed`, the `sample` call returns the duration since the `start`.   However, unlike `elapsed`, using `sample` doesn't stop timing.


### Named timing objects for gathering statistics
More complex scenarios, such as loops and complex control flows may easily require timing statistics to be gathered.   This can be done by using *named timing objects*, as in the following example.

```
    tobj = CodeTiming('MyCode')
    ...
    for i in range(...):
        ...
        tobj.start()
        ...
        cur_time = tobj.elapsed()
        ...
```
Statistics are gathered against the name "MyCode" so that each time the code between `start` and `elapsed` is executed, the measured duration will then contribute to the statistics for the named object "MyCode".  The `sample` method can be used to sample the timing (as shown earlier), but _without_ contributing to the timing statistics.

#### What about _nested_ timing? 
With _nested_ use of a timing object `tobj`, the pattern of use would look something like this:

```
    tobj = CodeTiming("MyTimer")
    ...
    tobj.start()      # start - outermost use of tobj
    ...
       ...
       tobj.start()      # start -- nested use of tobj
       ...
       tobj.elapsed()    # elapsed -- nested use of tobj
       ...
       
    ...
    tobj.elapsed()    # elapsed - outermost use of tobj
    ...
```

Any inner nested uses of the timing object `tobj` are included within the scope of the outermost timing period.   Therefore, to avoid "double counting",the inner nested uses of `tobj` are ignored and do not contribute to the statistics for `tobj`.


### Getting statistics info (1) -- `get_stats`

To access the current statistics for a timing object, use the function `get_stats`to obtain a dictionary containing the statistics info:

```
    stats_map = tobj.get_stats()
```

This returns a dictionary with the keys: `mean`, `std-dev`, `max`, `min`, `events` and `total`, as in this example:

```
     {'mean': 2504, 'std_dev': 2, 'max': 2507, 'min': 2501, 'events': 5, 'total': 12519}
```
where the entries are:
  
+  *mean*    -- Average of timings
+  *std_dev* -- Standard deviation of timings
+  *max*     -- Maximum timing
+  *min*     -- Minimum timing
+  *events*  -- Number of timing events measured
+  *total*   -- Total time measured

The timings above are given in milliseconds (default).  See the **Quick Reference** below for how to change the _timing unit_ (seconds or milliseconds).  


### Getting all statistics info (2) -- `get_stats_by_name`
The _classmethod_ `get_stats_by_name` takes a given name (e.g. "MyCode") and returns a dictionary containing the stats info for that named timing object.   This method fails if there is no timing object having the given name.

```
    my_code_stats = CodeTiming.get_stats_by_name("MyCode")
```


### Getting all statistics info (3) -- `get_all_stats`

Finally, the _classmethod_ `get_all_stats` provides a dictionary of named timing objects:

``` 
    timing_map = CodeTiming.get_all_stats()
```	

The resulting dictionary only contains entries for named timing objects having timing data -- timing objects with no timing data are omitted. 


### Convenience `display` utility functions

A number of `display` functions are provided to give a convenient textual rendering of the stats info as specified above. The display functions are:

+ **display\_stats** -- This function accesses the stats for a particular timing object and renders the information textually.

For example, if the stats info were:

```
    {'mean': 747, 'std_dev': 144, 'max': 974, 'min': 503, 'events': 30, 'total': 22409}
```

then the display would be:

```
     mean: 747ms, std_dev: (+ or -) 144ms, max: 974ms, min: 503ms, events: 30, total: 22s 409ms
```

+  **display\_stats\_by\_name** -- This _classmethod_ function accesses a named timing object specified by given name and displays the stats info textually.   Fails if there is no named timing object having the given name.

*  **display\_all\_stats** -- This _classmethod_ function extracts the stats info for named timing objects and displays the information in a table-like form.  As for `get_all_stats` only those named timimg objects having timing data are displayed -- timed objects having no timing data are omitted.

These functions broadly correspond to the various functions used for getting statistics described earlier.

#### Display keyword options
Each of the `display` functions outlined above use the same set of `keyword` arguments to specify display options.

- `hms` -- If True, format timing info in hrs-mins-secs-millisecs format (default: True).   Otherwise, format timings numerically in chosen units.

- `shape` -- Layout either _horizontally_ or _vertically_ (default: horizontal).

- `skip` -- Number of blank lines following (default: 0).


### Timing function calls -- Using the `@timing` decorator
The `@timing` decorator provides a way to time individual Python function codes.   Given a function definition, the `@timing` decorator adds a *named timing object* (with the same name as the function) to gather timing statistics of calls for that function.

```
    @timing
    def my_function(..., ...):
        ...
        return result  
    ...
    ... my_function( ... , ...) ...
    ...        
```
All (outermost) calls of timed functions like `my_function` contribute to their individual statistics. Because functions could be *recursively* defined (i.e. reentrant), timing of any inner calls is naturally included within the outermost call and therefore should **not** be measured separately. The `@timing` decorator approach dynamically tracks inner calls and avoids the inaccuracy due to the potential for "double-counting" these calls.

Since timed functions use named timed objects, the statistical timing info for those functions can be retrieved using classmethods `get_stats_by_name` or `get_all_stats` mentioned earlier.

### Using timing objects in with-statements

Named timing objects can be used in Python's _with-statements_.  The _with-statement_ provides a specific scope within which timings are _implicitly_ taken of the code that is running.  The timing of that code doesn't need a timing object directly.  In particular, such timing objects must be named so that statistics can be retrieved, by using classmethods such as `get_stats_by_name` or `display_stats_by_name` mentioned earlier.

```
    with CodeTiming("TestCode"):
        ...
        # code in scope being timed
        ...
        ...
   
    ...
    print(CodeTiming.get_stats_by_name("TestCode"))
    print(CodeTiming.display_stats_by_name("TestCode"))
    ...
```
_Note:_  Fails if the timing object is _anonymous_ (i.e. unnamed).   This is because it would be impossible to access anonymous timing objects  



### Using `autostart`

Timing objects can also be used in `autostart` mode.  This is where timing begins when the object is created and then automatically restarts following calls to `elapsed`.   The `start` method can still be called and simply _restarts_ the timing.   The `sample` method works as before and doesn't affect the statistics gathered.

The pattern of use with `autostart` goes as follows:

```
    tobj = CodeTiming(autostart=True)
    ...
    cur_time = tobj.elapsed()  # first timing
    ...
    cur_time = tobj.elapsed()  # second timing
    ...
```

Note that, in `autostart` mode, the `start` method is not necessary to begin timing -- that happens automatically when the timing object enters `autostart` mode.

---
# Quick Reference
This section gives a quick summary of the utilities provided.


## `CodeTiming`
Class providing utilities for timing Python code.

```
class CodeTiming

__init__ (self, name="", timeunit=MILLISECS_TIMEUNIT, timetype=TOTAL_TIMETYPE, autostart=False) 
```

+ `name` -- Optional name of timing object (default : "").   Unnamed (or _anonymous_) timing objects are _independent_ of each other.  There may be several instances of a timing object, named or unnamed.  However, the statistics for all instances of a named timing object with the same name will be aggregated together.

+ `timeunit` -- Unit of time measurement - either seconds or milliseconds (default: milliseconds).

+ `timetype` -- Type of time measurement (default : total).

   Types available are:
	  + `total`   -- Total system time
	  + `process` -- Process time
	  + `thread`  -- Thread time 

+ `autostart` -- If True, timing object is in `autostart` mode (default: False).
	
	When in autostart mode, timing starts immediately at creation of the timing object and continues indefinitely.


### Class Constants
These class constants give standard options (as strings) for various keyword options.  Strings are used instead of Enum's to simplify APIs.

```
	# Timetypes
	TOTAL_TIMETYPE =   "total timetype"
	PROCESS_TIMETYPE = "process timetype"
	THREAD_TIMETYPE =  "thread timetype"
	
	# Timeunits
	SECONDS_TIMEUNIT =   "seconds _timeunit"
	MILLISECS_TIMEUNIT = "millisecs _timeunit"
	
	# Display shape options
	DISPLAY_HORIZONTALLY = "horizontal"
	DISPLAY_VERTICALLY =   "vertical"
```

### Class Parameters
These class parameters affect the behaviour of timing objects in general.

```
	# If not None, this sets the timeunit globally
	GLOBAL_TIMEUNIT = None
	
	# If not None, this sets the timetype globally
	GLOBAL_TIMETYPE = None
	
    # Timeunit for function timing decorator.
    FUNCTION_TIMEUNIT = None 
    
    # Timetype for function timing decorator.
    FUNCTION_TIMETYPE = None 
	
	# Global enable
	GLOBAL_ENABLE = True
```

### Timing Methods
These methods provide the timing capabilities for the timing object.

#### start
Initiates timing for timing object. In autostart mode, this restarts timing.

```
    def start(self)
```

_Note:_ to avoid misleading results, any nested uses of a timing object is detected and doesn't contribute to statistics -- only the outermost use of a timing object is recorded.


#### elapsed
Measures duration since the current start, and _stops_ timing -- except in autostart mode, when instead timing continues. By using `elapsed`, the durations it measures contribute to calculating timing statistics (for both named and anonymous timing objects).   Returns the duration measured (or `None` if timing not started or disabled).

```
    def elapsed(self)
```

#### sample
Returns duration since the current start -- but doesn't contribute to the statistics for the timing object.  This could return `None` if timing not started or disabled.

```
    def sample(self)
```

### Stats Access Methods
Statistics are gathered for all timing objects.   The methods listed here 


#### get\_stats
Produces a dictionary object representing the statistical information gathered by the timing object.

```
	def get_stats(self)
```

The fields are `mean, std_dev, max, min, events, total` and defined as:
  
+  `mean`    -- Average of timings
+  `std_dev` -- Standard deviation of timings
+  `max`     -- Maximum timing
+  `min`     -- Minimum timing
+  `events`  -- Number of timing events measured
+  `total`   -- Total time measured

#### get\_stats\_by\_name
This classmethod accesses the named timing object as specified by given name and, if found, produces a dictionary object as described above.  Fails if no named timing object exists with given name.

```
	@classmethod
    def get_stats_by_name(_, name)
```

#### get\_all\_stats
This classmethod produces a dictionary, keyed by name, of corresponding stats dictionary objects for named timing objects.  Entries are only given for each named timing object having timing data -- others not having any timing data are omitted.

```
	@classmethod
    def get_all_stats(_)
```

### Stats Display Methods
As a convenience, a number of display methods are provided for rendering the statistics information for timing objects as strings.  These broadly correspond to the various stats access methods given earlier.

#### display_stats
Renders as a string the dictionary object representing the statistical information gathered by the timing object.

```
	def display_stats(self, hms=True, shape=DISPLAY_HORIZONTALLY, skip=0)
```
The keyword arguments are common for all three of these display functions:

- `hms` -- If True, format timing info in a "h m s ms" structured format (default: True).   Otherwise, format timings numerically in chosen units.

- `shape` -- Layout either _horizontally_ or _vertically_ (default: horizontal).

- `skip` -- Number of blank lines following (default: 0).

__Note:_ In vertical layout, the minimum skip value is set to 1 to ensure separation of entries.

_Note:_ _HMS format_ This displays timing information in a structured, easily readable format.   For example:

```
        4s 23ms            (4023 msecs)
        2h 14m 31s 257ms   (8071257 msecs)
```

#### display\_stats\_by\_name
This classmethod accesses the named timing object specified by given name and, if found, renders as a string the associated dictionary object as described above.  Fails if no named timing object exists with given name.

```
	@classmethod
    def display_stats_by_name(_, name, hms=True, shape=DISPLAY_HORIZONTALLY, skip=0)
```


#### display\_all\_stats
This classmethod renders as a string the table, keyed by name, of corresponding stats dictionary objects for named timing objects.  Entries are only given for each named timing object having timing data -- others not having any timing data are omitted.

```
	@classmethod
    def display_all_stats(_, hms=True, shape=DISPLAY_HORIZONTALLY, skip=0)
```
### State Setter Methods
These methods are used to configure timing objects.

#### reset\_all
This classmethod resets the state of all named timimg objects.  Any timing objects in autostart mode are restarted.

```
    @classmethod
    def reset_all(_): 
```

#### reset
This resets the state of a specific timing object.  Objects in autostart mode are restarted.

```
	def reset(self)
```

#### set\_autostart
Sets autostart mode and restarts timing (default : False).   Fails if timing has already begun.  This method returns `self` to enable chaining of setter methods.

```
	def set_autostart(self)
```

#### set\_enabled
This is used to enable or disable the timing object (default: enabled).  Disabling the object means that statistics are not gathered and that the methods `enabled` and `sample` return `None`.  This method returns `self` to enable chaining of setter methods.

```
	def set_enabled(self, flag)
```

#### set\_name
This associates a name with a currently anonymous timing object (i.e. with empty name).  This is coordinated so  that looking up the object by name (e.g. `get_stats_by_name`) and accessing it directly (e.g. `get_stats`) produces the same behaviour.  Fails if the object is already named.  This method returns `self` to enable chaining of setter methods.

```
	def set_name(self, new_name)
```
_Note:_ The names of named objects need not be *uniquely* defined - that is, there may be several instances of a timed object each one having the same name.  _However, in all such cases, the resulting object are all alike._ This means that the statistics gathered by each instance is aggregated with others of the same name.

_Note_ Chaining of methods allows for directly applying chaining methods one after the other:

```
	tobj = CodeTiming()
	...
	tobj.set_autostart().set_name("MyTimer")
``` 


# LICENSE

MIT License

Copyright (c) 2023 Purple Elephant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# **`Tests` Directory**
> This directory is for written unit tests. Which will be automatically executed during a Git commit, and ensure that the any written code will be error/bug free (as long as the tests are suitable).
>
> This guide will be split into two sections, that shouldn't be too long.
>
>> **Testing Guide**
>> 
>> This section is a general-use guide for testing.
>
>> **Testing Workflow**
>>
>> This section will describe how things are to be done, to ensure that testing is done effectively.

<br><br>

# **Testing Guide**
> ## **Manual Testing**
> 1. Run `pytest` in the terminal
> 
> ## **Coverage Report**
> 1. As described within `/README.md`; to open the coverage report, select `.coverage`, press bottom-right `Go Live` button, navigate to `htmlcov` once the live server is open.
> 2. The coverage report has three sections: `Files`, `Functions` and `Classes`.
> 3. `Files` is a general overview of the coverage of all the `src` code, that the `tests` code had reached. Or in simpler words, how many lines of codes has been ran at least once, for each `src` file.
> 4. `Functions` is an overview for the coverage, of each function within each file.
> 5. `Classes` is an overview for the coverage, of each class within each file.
> 6. Selecting a file will show which and how many lines, have be ran, missed, and excluded during testing.
> 7. To return to the overview, press `^ index`. To cycle through the files press `<<prev` or `>> next`.

<br><br>

# **Testing Workflow**
> The format of this will most be different, because it will just go through how the testing workflow is to be done. It shouldn't be too complicated however.
>
> **All Non-Test** code is to be saved in `/src`, mostly for organisation purposes.
>
> **All Test** code is to be saved in `/tests`. They should be named appropriately; or just go with naming the files as `test_<related /src file name>`, for simplicity and convenience.
>
> **All Test** code are to be written with `def` functions, named something similar like `test_<task to test>`.
>
> As for **Coverage**, it **Isn't Required** to have 100% coverage (and tbh I'm unsure whether a coverage report would be required, like from our previous modules). So, though it is preferable, it won't be mandated or anything.
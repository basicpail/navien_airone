# navien_airone
configuration.yaml for navien

```
  input_select:
    navien_select_option_gv:
      options:
        - nothing
        - turbo
        - powersaving
    navien_select_option_ac:
      options:
        - nothing
        - turbo
        - powersaving
    navien_select_windlevel_gv:
      options:
        - notset
        - weakwind
        - heavywind
        - mightywind
    navien_select_windlevel_ac:
      options:
        - notset
        - weakwind
        - heavywind
        - mightywind
    navien_select_schedule:
      options:
        - enable_power_off
        - enable_power_on

  input_text:
    navien_schedule_input:
      initial: ex)17:20
    navien_deepsleep_start_input:
      initial: ex)17:20
    navien_deepsleep_end_input:
      initial: ex)17:20
      
```

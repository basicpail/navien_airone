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

```
- type: entities
        entities:
          - sensor.navien_aireone_current_operationmode
          - sensor.navien_aireone_currenttemperature
          - sensor.navien_aireone_desiredhumidity
          - switch.navien_aireone_power
          - type: 'custom:fold-entity-row'
            head:
              type: section
              label: General_Ventilation
            entities:
              - input_select.navien_select_option_gv
              - input_select.navien_select_windlevel_gv
              - type: button
                entity: switch.navien_aireone_general_ventilation
          - type: 'custom:fold-entity-row'
            head:
              type: section
              label: Air_Cleaning
            entities:
              - input_select.navien_select_option_ac
              - input_select.navien_select_windlevel_ac
              - type: button
                entity: switch.navien_aireone_air_cleaning
          - type: 'custom:fold-entity-row'
            head:
              type: section
              label: Automatic_Operation
            entities:
              - type: button
                entity: switch.navien_aireone_automatic_operation
          - type: 'custom:fold-entity-row'
            head:
              type: section
              label: Schedule
            entities:
              - input_select.navien_select_schedule
              - input_text.navien_schedule_input
              - switch.navien_aireone_schedule
          - type: 'custom:fold-entity-row'
            head:
              type: section
              label: Deep-Sleep
            entities:
              - input_text.navien_deepsleep_start_input
              - input_text.navien_deepsleep_end_input
              - switch.navien_aireone_deep_sleep
```

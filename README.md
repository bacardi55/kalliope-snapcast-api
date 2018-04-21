# Kalliope Snapcast API

## Synopsis

Allow [Kalliope](https://kalliope-project.github.io/) to interact with [Snapcast](https://github.com/badaix/snapcast) [API](https://github.com/badaix/snapcast/blob/master/doc/json_rpc_api/v2_0_0.md#clientsetvolume).

This neuron doesn't coverage the whole API of snapcast. It only manage client volume and mute/unmute system so far.
I'm happy to add more coverage if people need it or accept pull requests :).

I plan to add a second stream on snapcast at some point so i will update it some day^^.

## Installation
```bash
kalliope install --git-url https://github.com/bacardi55/kalliope-snapcast-api.git
```

## Options

(usage of a [table generator](http://www.tablesgenerator.com/markdown_tables) is recommended)

| parameter        | required | default     | choices                            | comments                                 |
|------------------|----------|-------------|------------------------------------|------------------------------------------|
| action           | yes      |             | set_volume, mute, unmute           | The action choice                        |
| mac address      | yes      | *           | A list of mac address or * for all | A list of mac address of snapcast client |
| volume           | no       | 55          | Volume number                      | Required only if action is set_volume    |
| host             | yes      | 192.168.1.2 | Volume number                      | Required only if action is set_volume    |
| port             | yes      | 1705        | Volume number                      | Required only if action is set_volume    |


## Return Values

No return value


## Synapses example

Description of what the synapse will do
```yml
  - name: "snapcast-set-volume-all"
    signals:
      - order: "Volume global de music à {{volume}}"
    neurons:
      - snapcastapi:
          action: 'volume'
          mac_addresses: '*'
          volume: '{{volume}}'
          host: '{{snapcast_host}}'
          port: '{{snapcast_port}}'

  - name: "snapcast-set-volume-client"
    signals:
      - order: "Set music volume at 55 in the kitchen"
    neurons:
      - snapcastapi:
          action: 'volume'
          mac_addresses:
              - '{{snapcast_brook}}'
          host: '{{snapcast_host}}'
          port: '{{snapcast_port}}'

  - name: "snapcast-mute-all"
    signals:
      - order: "Mute music everywhere"
    neurons:
      - snapcastapi:
          action: 'mute'
          mac_addresses: '*'
          host: '{{snapcast_host}}'
          port: '{{snapcast_port}}'

  - name: "snapcast-unmute-all"
    signals:
      - order: "Unmute music everywhere"
    neurons:
      - snapcastapi:
          action: 'unmute'
          mac_addresses: '*'
          host: '{{snapcast_host}}'
          port: '{{snapcast_port}}'

  - name: "snapcast-mute-client"
    signals:
      - order: "Mute the music in the kitchen"
    neurons:
      - snapcastapi:
          action: 'mute'
          mac_addresses: 
              - '{{snapcast_brook}}'
          host: '{{snapcast_host}}'
          port: '{{snapcast_port}}'

  - name: "snapcast-unmute-client"
    signals:
      - order: "unmute the music in the kitchen"
    neurons:
      - snapcastapi:
          action: 'unmute'
          mac_addresses:
              - '{{snapcast_brook}}'
          host: '{{snapcast_host}}'
          port: '{{snapcast_port}}'
```


Use [private variable file](https://github.com/kalliope-project/kalliope/blob/master/Docs/settings.md#global-variables).

# CROC Tools

### Setup `croc_tools`
```sh
git clone https://github.com/fstaeg/croc_tools.git
cd croc_tools
source setup.sh
```
- `setup.sh` makes the scripts executable and adds the `croc_tools` directory to `$PATH`, so they can be run from within the run directory in `Ph2_ACF` (or anywhere else)
 
 
### `mux_vdd.py`

Measure `VDDA`, `VDDD` using the ADC:
- ADC conversion to volts/amps
  - `voltage (mV) = VMux * slope + offset`
  - `current (mA) = (IMux * slope + offset) / 4990`
- Look up `slope` and `offset` for each chip in the wafer probing data and add them to the function `ADCtoVoltage` in `adc_tools.py`
- From the run directory in `Ph2_ACF`, run `MuxScan`: `RD53BminiDAQ -f CROC.xml -t RD53BTools.toml -h MuxScan`
- `mux_vdd.py -m {MODULE} -i Results/MuxScan`
  - If directory `Results/MuxScan` already exists, the results of the MuxScan are to `Results/MuxScan_1` etc


### `probecard_readout.py`

Measure `VIN`, `VDDA`, `VDDD` using the needle probe card:
- Put the IP of your Raspberry Pi in `probecard_readout.py`
- Run: `probecard_readout.py [-f filename.csv]`
  - take 5 measurements of `VIN`, `VDDA`, `VDDD` (for each chip), calculate the average and standard deviation, and save them to `filename.csv`
  - without `-f`: take a measurement every 3 seconds and print it to the Terminal


### `root_plotting.py`

Plots produced by a tool in `Ph2_ACF` are saved in a ROOT file `Results/{TOOL_NAME}/results.root`. This script can be used to save all plots in `results.root` as PDF or PNG files:
```sh
root_plotting.py Results/{TOOL_NAME} [--png]
```


### `mux_needle_plotting.py`

Produces plots for characterization of CROC modules (I-V-curves, current overhead, comparison of VMUX and Needle Card measurements, ...)
```sh
mux_needle_plotting.py
```




## Ph2_ACF instructions

### Install Ph2_ACF

Install the Ph2_ACF software from https://gitlab.cern.ch/alpapado/Ph2_ACF

- Software that has to be installed first: 
  - `epel-release`, `pugixml-devel`, `boost-devel`, `centos-release-scl`, `devtoolset-10` (install using `sudo yum install`)
  - [`CERN ROOT`](https://root.cern.ch/), [`IPBus`](http://ipbus.web.cern.ch/ipbus) (install from source)
- Clone git repo:
```sh
git clone --recurse-submodules https://gitlab.cern.ch/alpapado/Ph2_ACF.git
```
- Compile:
```sh
cd Ph2_ACF; source setup.sh; mkdir myBuild; cd myBuild
cmake ..; make -j8; cd ..
```
- Set up a directory to run the software from and copy the necessary configuration files there:
  - `mkdir rundir`
  - Hardware description file: `cp settings/CROC.xml rundir`
  - Tools configuration file: `cp settings/RD53BTools.toml rundir`
  - `cp settings/RD53B.toml rundir; cd rundir`


### Install FC7 manager

To set up communication with the FC7, install fc7-manager from https://gitlab.cern.ch/alpapado/fc7-manager

- Upgrade pip and setuptools:
```sh
curl "https://bootstrap.pypa.io/pip/2.7/get-pip.py" | sudo python2
sudo pip2 install "setuptools>=44,<45"
```
- Install fc7-manager:
```sh
sudo pip2 install --no-binary :all: git+https://gitlab.cern.ch/alpapado/fc7-manager.git
```


### Firmware setup

- Download the latest version of the firmware from https://gitlab.cern.ch/cmstkph2-IT/d19c-firmware/-/tags
- Upload the `.bit` file to the microSD card that is plugged into the FC7:
```sh
fpgaconfig -c CROC.xml -f firmware_file_name_on_the_PC -i fw_file_name_on_the_microSD
```
- Configure the FPGA with that firmware image:
```sh
fpgaconfig -c CROC.xml -i fw_file_name_on_the_microSD
```
- To list all the firmware images already stored on the microSD:
```sh
fpgaconfig -c CROC.xml -l
```


### Use the software

- `cd Ph2_ACF; source setup.sh; cd rundir`
- Configure FPGA with firmware image: `fpgaconfig -c CROC.xml -i fw_file_name_on_the_microSD`
- Reset chip: `RD53BminiDAQ -f CROC.xml -r`
- Run any tool: `RD53BminiDAQ -f CROC.xml -t RD53BTools.toml [-h] [-s] {TOOL}`
  - `-h`: do not display plots that are created
  - `-s`: update the chip configuration file (needed when doing any kind of tuning)







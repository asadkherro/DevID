// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    struct Device {
        bytes32 id;
        string name;
        string ip_address;
        string mac_address;
        string runningDevice;
        string os_cpe;
        string os_details;
        string os_guesses;
    }

    Device[] private devices;
    mapping(bytes32 => uint256) private idToIndex;
    mapping(string => bytes32) private macToId;
    uint256 private counter;

    event DeviceAdded(bytes32 id, string name, string ip_address, string mac_address, string runningDevice, string os_cpe, string os_details, string os_guesses);
    event DeviceUpdated(bytes32 id, string name, string ip_address, string mac_address, string runningDevice, string os_cpe, string os_details, string os_guesses);
    event DeviceDeleted(bytes32 id);

    function set(
        string memory name,
        string memory ip_address,
        string memory mac_address,
        string memory runningDevice,
        string memory os_cpe,
        string memory os_details,
        string memory os_guesses
    ) public returns (bytes32) {
        require(bytes(name).length > 0, "Name is required");
        require(bytes(ip_address).length > 0, "IP Address is required");
        require(bytes(mac_address).length > 0, "MAC Address is required");

        // Check if device with the same MAC address already exists
        if (macToId[mac_address] != bytes32(0)) {
            return macToId[mac_address];
        }

        counter++;
        bytes32 id = keccak256(abi.encodePacked(block.timestamp, msg.sender, counter));
        devices.push(Device(id, name, ip_address, mac_address, runningDevice, os_cpe, os_details, os_guesses));
        idToIndex[id] = devices.length - 1;
        macToId[mac_address] = id;
        emit DeviceAdded(id, name, ip_address, mac_address, runningDevice, os_cpe, os_details, os_guesses);
        return id;
    }

    function getDeviceById(bytes32 id) public view returns (Device memory) {
        require(idToIndex[id] < devices.length, "Device not found");
        return devices[idToIndex[id]];
    }

    function getDeviceByMacAddress(string memory mac_address) public view returns (Device memory) {
        bytes32 id = macToId[mac_address];
        require(id != bytes32(0), "Device not found");
        return devices[idToIndex[id]];
    }

    function getAllDevices() public view returns (Device[] memory) {
        return devices;
    }

    function updateDevice(
        bytes32 id,
        string memory name,
        string memory ip_address,
        string memory mac_address,
        string memory runningDevice,
        string memory os_cpe,
        string memory os_details,
        string memory os_guesses
    ) public {
        require(idToIndex[id] < devices.length, "Device not found");
        
        Device storage device = devices[idToIndex[id]];
        
        // Update device information
        if (bytes(name).length > 0) {
            device.name = name;
        }
        if (bytes(ip_address).length > 0) {
            device.ip_address = ip_address;
        }
        if (bytes(mac_address).length > 0) {
            // Update the MAC address mapping
            delete macToId[device.mac_address];  // Remove old MAC address mapping
            macToId[mac_address] = id;
            device.mac_address = mac_address;
        }
        if (bytes(runningDevice).length > 0) {
            device.runningDevice = runningDevice;
        }
        if (bytes(os_cpe).length > 0) {
            device.os_cpe = os_cpe;
        }
        if (bytes(os_details).length > 0) {
            device.os_details = os_details;
        }
        if (bytes(os_guesses).length > 0) {
            device.os_guesses = os_guesses;
        }

        emit DeviceUpdated(id, device.name, device.ip_address, device.mac_address, device.runningDevice, device.os_cpe, device.os_details, device.os_guesses);
    }

    function deleteDeviceById(bytes32 id) public {
        require(idToIndex[id] < devices.length, "Device not found");

        uint256 index = idToIndex[id];
        Device memory device = devices[index];

        // Remove the device by swapping with the last device and then popping
        if (index < devices.length - 1) {
            devices[index] = devices[devices.length - 1];
            idToIndex[devices[index].id] = index;
        }
        devices.pop();
        delete idToIndex[id];
        delete macToId[device.mac_address];
        
        emit DeviceDeleted(id);
    }
}

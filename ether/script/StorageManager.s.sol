pragma solidity ^0.8.13;

import {Script, console2} from "forge-std/Script.sol";
import {StorageManager} from "../src/StorageManager.sol";

contract StorageManagerScript is Script {
    function setUp() public {}

    function run() public {
        uint pk = vm.envUint("PRIVATE_KEY");
        address me = vm.addr(pk);

        console2.log(me);

        vm.startBroadcast(pk);

        StorageManager sm = new StorageManager();
        // console2.log(sm);
        
        vm.stopBroadcast();
    }
}

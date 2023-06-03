// Chakra imports
import { Box, Flex, Grid, Icon } from "@chakra-ui/react";
import React from "react";


function RealtimePrediction() {
  return (
    <Flex direction='column' pt={{ base: "120px", md: "75px" }} height="100%">
      <iframe allow="camera;microphone" src="http://localhost:8080/"></iframe>
    </Flex>
  );
}

export default RealtimePrediction;

import {
  Flex,
  useColorModeValue,
  Input,
  Button,
  FormControl,
  Image,
  FormLabel,
  Box,
  UnorderedList,
  ListItem,
} from "@chakra-ui/react";
import {DeleteIcon} from "@chakra-ui/icons"
import React, { useState, useRef, useEffect } from "react";
import api from "api/api";

export default function PhotoPrediction() {
  const iconBoxInside = useColorModeValue("white", "white");
  const [selectedFile, setSelectedFile] = useState("");
  const [predictedImages, setPredictedImages] = useState([]);

  const imageRef = useRef();

  const fileChangeHandler = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const apiRequest = (e) => {
    const formData = new FormData();
    formData.append("image_file", selectedFile);
    api.image
      .predict(selectedFile.name.split(".")[0], formData)
      .then((res) => {
        console.log(res.data);
        imageRef.current.src = `http://localhost:8000/image_detection/${selectedFile.name.split(".")[0]}`;
        api.image.list_images().then((res) => {
          setPredictedImages(res.data);
        });
      })
      .catch((e) => console.log(e));
  };

  useEffect(() => {
    api.image.list_images().then((res) => {
      setPredictedImages(res.data);
    });
  }, []);

  const handleDeleteImage = (item) => {
    api.image.delete(item).then(() => {
      api.image.list_images().then((res) => {
        setPredictedImages(res.data);
      });
    });
  };

  return (
    <Flex
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      pt={{ base: "120px", md: "75px" }}
      height="100vh" // Добавлено свойство height
    >
      <FormControl width="20%">
        <FormLabel>Select an image for prediction</FormLabel>
        <Input onChange={fileChangeHandler} type="file" accept=".jpeg, .jpg, .png" />
        <Button onClick={apiRequest} mt={4} colorScheme="teal">
          Get prediction
        </Button>
      </FormControl>
      <Flex mt={8} alignItems="center">
        <Box>
          <FormLabel>Predicted Image</FormLabel>
          <Image
            style={{ clear: "both" }}
            width="100%"
            ref={imageRef}
            src=""
            alt="Predicted Image"
            fallbackSrc="https://via.placeholder.com/500"
          />
        </Box>
        <Box ml={8}>
          <Box mb={2}>
            <FormLabel>Previous Predictions</FormLabel>
          </Box>
          <UnorderedList>
            {predictedImages.map((item) => (
              <ListItem key={item} display="flex" alignItems="center">
                <Image
                  onClick={() => {
                    imageRef.current.src = `http://localhost:8000/image_detection/${item}`;
                  }}
                  src={`http://localhost:8000/image_detection/${item}`}
                  boxSize="50px"
                  objectFit="cover"
                  borderRadius="md"
                  mr={2}
                />
                <Box>{item}</Box>
                <Button
                  onClick={() => {
                    handleDeleteImage(item);
                  }}
                  leftIcon={<DeleteIcon />}
                  colorScheme="red"
                  variant="outline"
                  size="sm"
                  ml={2}
                >
                  Delete
                </Button>
              </ListItem>
            ))}
          </UnorderedList>
        </Box>
      </Flex>
    </Flex>
  );
}
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
  Select,
  InputGroup,
  InputRightElement,
  CloseButton,
} from "@chakra-ui/react";
import { DeleteIcon, ViewIcon, SearchIcon } from "@chakra-ui/icons";
import React, { useState, useRef, useEffect } from "react";
import api from "api/api";

export default function PhotoPrediction() {
  const iconBoxInside = useColorModeValue("white", "white");
  const [selectedFile, setSelectedFile] = useState("");
  const [predictedImages, setPredictedImages] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

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

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredImages = predictedImages.filter((item) =>
    item.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Flex minHeight="100vh" alignItems="stretch" justifyContent="center" paddingLeft="100">
      <Box width="70%">
        <Flex alignItems="center" paddingTop="100">
          <FormControl width="40%">
            <FormLabel>Выберите фотографию для распознавания</FormLabel>
            <Input onChange={fileChangeHandler} type="file" accept=".jpeg, .jpg, .png" />
            <FormLabel>Разрешение фотографии</FormLabel>
            <Select>
              <option value="option1">1280x720</option>
              <option value="option2">1920x1080</option>
              <option value="option3">640x480</option>
            </Select>
            <Button onClick={apiRequest} mt={4} colorScheme="teal">
              Загрузить фотографию
            </Button>
          </FormControl>
        </Flex>
        <Box mt={8}>
          <FormLabel>Просмотр фотографии</FormLabel>
          <Image
            style={{ clear: "both" }}
            width="100%"
            ref={imageRef}
            src=""
            alt="Predicted Image"
            fallbackSrc="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/681px-Placeholder_view_vector.svg.png"
          />
        </Box>
      </Box>
      <Box width="30%" ml={8} position="relative" paddingTop="100px">
        <Box mb={2} display="flex" alignItems="center">
          <FormLabel>Загруженные фотографии</FormLabel>
          <InputGroup ml={2} flex="1" maxW="md">
            <Input
              placeholder="Поиск"
              value={searchTerm}
              onChange={handleSearch}
              pr="4.5rem"
              borderRadius="md"
            />
            <InputRightElement width="4.5rem">
              {searchTerm && (
                <CloseButton
                  size="sm"
                  onClick={() => setSearchTerm("")}
                  _focus={{ boxShadow: "none" }}
                />
              )}
              <SearchIcon color="gray.400" />
            </InputRightElement>
          </InputGroup>
        </Box>
        <Box height="calc(100% - 46px)" overflowY="auto">
          <UnorderedList>
            {filteredImages.map((item) => (
              <ListItem
                key={item}
                display="flex"
                alignItems="center"
                _hover={{ bg: useColorModeValue("gray.100", "gray.800") }}
                p={2}
                borderRadius="md"
                cursor="pointer"
              >
                <Image
                  src={`http://localhost:8000/image_detection/${item}`}
                  boxSize="50px"
                  objectFit="cover"
                  borderRadius="md"
                  mr={2}
                />
                <Box>{item}</Box>
                <Button
                  onClick={() => {
                    imageRef.current.src = `http://localhost:8000/image_detection/${item}`;
                  }}
                  leftIcon={<ViewIcon />}
                  variant="outline"
                  size="sm"
                  ml={2}
                >
                  Просмотр
                </Button>
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
                  Удалить
                </Button>
              </ListItem>
            ))}
          </UnorderedList>
        </Box>
      </Box>
    </Flex>
  );
}

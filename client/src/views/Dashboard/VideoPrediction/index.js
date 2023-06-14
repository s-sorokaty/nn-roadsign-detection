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
  Video,
  InputGroup,
  InputRightElement,
  CloseButton,
  Select
} from "@chakra-ui/react";
import { DeleteIcon, SearchIcon,ViewIcon } from "@chakra-ui/icons";
import React, { useState, useRef, useEffect } from "react";
import api from "api/api";

export default function VideoPrediction() {
  const iconBoxInside = useColorModeValue("white", "white");
  const [selectedFile, setSelectedFile] = useState("");
  const [predictedVideos, setPredictedVideos] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false)


  const videoRef = useRef();

  const fileChangeHandler = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const apiRequest = (e) => {
    setIsLoading(true)
    const formData = new FormData();
    formData.append("video_file", selectedFile);
    api.video
      .predict(selectedFile.name.split(".")[0], formData)
      .then((res) => {
        console.log(res.data);
        videoRef.current.src = `http://localhost:8000/video_stream/${selectedFile.name.split(".")[0]}`;
        api.video.list_videos().then((res) => {
          setIsLoading(false)
          setPredictedVideos(res.data);
        });
      })
      .catch((e) => console.log(e));
  };

  useEffect(() => {
    api.video.list_videos().then((res) => {
      setPredictedVideos(res.data);
    });
  }, []);

  const handleDeleteVideo = (item) => {
    api.video.delete(item).then(() => {
      api.video.list_videos().then((res) => {
        setPredictedVideos(res.data);
      });
    });
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredVideos = predictedVideos.filter((item) =>
    item.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Flex alignItems="stretch" justifyContent="center"  paddingTop="100">
      <Box width="70%">
        <FormControl width="40%" alignItems="center">
          <FormLabel textAlign="left">Видео для предсказания</FormLabel>
          <Input onChange={fileChangeHandler} type="file" accept=".mp4, .webm" />
          <FormLabel>Разрешение видео</FormLabel>
            <Select>
              <option value="option1">1280x720</option>
              <option value="option2">1920x1080</option>
              <option value="option3">640x480</option>
            </Select>
          <FormLabel>Колличество кадров в секунду</FormLabel>
            <Select>
              <option value="option1">30</option>
              <option value="option5">10</option>
              <option value="option2">15</option>
              <option value="option3">20</option>
              <option value="option4">25</option>
          </Select>
          <Button isLoading={isLoading} onClick={apiRequest} mt={4} colorScheme="teal">
            Загрузить видео
          </Button>
        </FormControl>
        <Box mt={8}>
          <FormLabel>Просмотр видео</FormLabel>
          <Box
            as="video"
            controls
            style={{ clear: "both" }}
            width="100%"
            ref={videoRef}
            src=""
            alt="Predicted Video"
            fallbackSrc="https://via.placeholder.com/500"
          />
        </Box>
      </Box>
      <Flex mt={{ base: 8, md: 0 }} ml={{ base: 0, md: 8 }} flexDirection="column">
        <Box mt={8}>
          <Box mb={2} display="flex" alignItems="right" justifyContent="space-between">
            <FormLabel>Ваши видео</FormLabel>
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
              {filteredVideos.map((item) => (
                <ListItem
                  key={item}
                  display="flex"
                  alignItems="center"
                  _hover={{ bg: useColorModeValue("gray.100", "gray.800") }}
                  p={2}
                  borderRadius="md"
                  cursor="pointer"
                >
                  <Box
                    as="video"
                    src={`http://localhost:8000/video_stream/${item}`}
                    boxSize="50px"
                    objectFit="cover"
                    borderRadius="md"
                    mr={2}
                  />
                  <Box>{item}</Box>
                  <Button
                  onClick={() => {
                    videoRef.current.src = `http://localhost:8000/video_stream/${item}`;
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
                      handleDeleteVideo(item);
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
    </Flex>
  );
}

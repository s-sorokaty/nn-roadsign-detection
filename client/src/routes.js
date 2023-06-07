import PhotoPrediction from "views/Dashboard/PhotoPrediction";
import VideoPrediction from "views/Dashboard/VideoPrediction";
import RealtimePrediction from "views/Dashboard/RealtimePrediction";
import {Image} from "@chakra-ui/react"
import {ViewIcon} from "@chakra-ui/icons"

import {
  HomeIcon,
  StatsIcon,
  CreditIcon,
} from "components/Icons/Icons";

var dashRoutes = [
  {
    path: "/photo-prediction",
    name: "Распознавание на фотографии",
    icon: <Image src="https://cdn.icon-icons.com/icons2/510/PNG/512/image_icon-icons.com_50366.png" />,
    component: PhotoPrediction,
    layout: "/admin",
  },
  {
    path: "/video-prediction",
    name: "Распознавание на видео",
    icon: <Image src="https://w7.pngwing.com/pngs/375/969/png-transparent-computer-icons-video-cameras-video-icon-angle-rectangle-photography.png" />,
    component: VideoPrediction,
    layout: "/admin",
  },
  {
    path: "/realtime-prediction",
    name: "Распознавание в реальном времени",
    icon: <Image src="https://w7.pngwing.com/pngs/639/614/png-transparent-computer-icons-camera-camera-photography-rectangle-camera-icon-thumbnail.png" />,
    component: RealtimePrediction,
    layout: "/admin",
  },
];
export default dashRoutes;

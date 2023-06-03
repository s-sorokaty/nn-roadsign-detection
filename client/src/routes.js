import PhotoPrediction from "views/Dashboard/PhotoPrediction";
import VideoPrediction from "views/Dashboard/VideoPrediction";
import RealtimePrediction from "views/Dashboard/RealtimePrediction";

import {
  HomeIcon,
  StatsIcon,
  CreditIcon,
} from "components/Icons/Icons";

var dashRoutes = [
  {
    path: "/photo-prediction",
    name: "Photo prediction",
    icon: <HomeIcon color="inherit" />,
    component: PhotoPrediction,
    layout: "/admin",
  },
  {
    path: "/video-prediction",
    name: "Video prediction",
    icon: <StatsIcon color="inherit" />,
    component: VideoPrediction,
    layout: "/admin",
  },
  {
    path: "/realtime-prediction",
    name: "Realtime prediction",
    icon: <CreditIcon color="inherit" />,
    component: RealtimePrediction,
    layout: "/admin",
  },
];
export default dashRoutes;

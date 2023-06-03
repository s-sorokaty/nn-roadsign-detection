// import
import PhotoPrediction from "views/Dashboard/PhotoPrediction";
import Tables from "views/Dashboard/Tables";
import Billing from "views/Dashboard/Billing";

import {
  HomeIcon,
  StatsIcon,
  CreditIcon,
  PersonIcon,
  DocumentIcon,
  RocketIcon,
  SupportIcon,
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
    component: Tables,
    layout: "/admin",
  },
  {
    path: "/realtime-prediction",
    name: "Realtime prediction",
    icon: <CreditIcon color="inherit" />,
    component: Billing,
    layout: "/admin",
  },
];
export default dashRoutes;

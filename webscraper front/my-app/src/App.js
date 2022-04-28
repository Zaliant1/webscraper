import React from "react";
import "./App.css";

import { BrowserRouter, Route, Routes, Link, Outlet } from "react-router-dom";
import MovieComponent from "./components/pages/movie.component";

import { Container } from "react-bootstrap";
import SearchComponent from "./components/pages/search.component";
import MovieDetails from "./components/pages/MovieDetails";
import CastMemberComponent from "./components/pages/CastDetails.component";

const HomePage = () => {
  return (
    <Container fluid="md">
      <h1>
        <Link to="/">Home Page</Link>
      </h1>
      <SearchComponent />
      <Outlet />
    </Container>
  );
};

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />}>
          <Route path="search/:title" element={<MovieComponent />} />
          <Route path="movie/:title" element={<MovieDetails />} />
          <Route path="cast/:castmember" element={<CastMemberComponent />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;

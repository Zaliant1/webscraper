import React from "react";
import { VCard } from "./cards";

export const CardList = ({ movies }) => {
  return (
    <React.Fragment>
      {movies.map((movie) => (
        <VCard
          key={`vcard-${movie.safe_title.toLowerCase().replace(" ", "-")}`}
          movie={movie}
        />
      ))}
    </React.Fragment>
  );
};

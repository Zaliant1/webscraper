import React, { useState, useEffect } from "react";
import { Row, Col, Card } from "react-bootstrap";

import { useParams } from "react-router-dom";

import { Cast } from "../card-list/cards";

const MovieDetails = () => {
  let { title } = useParams();

  const [movieDetails, setMovieDetails] = useState(false);

  useEffect(() => {
    fetch(`/movies/${title}/info`)
      .then((response) => response.json())
      .then((data) => setMovieDetails(data));
  }, [title]);

  if (movieDetails === false) {
    return <h3>populating movie details...</h3>;
  }

  return (
    <Card style={{ marginTop: "15px" }}>
      <Card.Body>
        <Row>
          <Col
            key={`card-${movieDetails.title}`}
            md="3"
            style={{
              marginBottom: "15px",
              marginTop: "15px",
              textAlign: "left",
            }}
          >
            <img
              src={movieDetails.cover}
              alt="..."
              width="208px"
              height="307px"
              border="1px solid #000"
            />
            <h3>{`${movieDetails.title}`}</h3>
            <p>
              Tomatometer
              <img
                src="https://www.rottentomatoes.com/assets/pizza-pie/images/icons/tomatometer/certified_fresh.75211285dbb.svg"
                alt="tomatometer icon"
                height="25px"
                width="25px"
              ></img>
              : {movieDetails.score}
            </p>
            <p>
              Audience Score
              <img
                src="https://www.rottentomatoes.com/assets/pizza-pie/images/icons/audience/aud_score-fresh.6c24d79faaf.svg"
                alt="audience score icon"
                height="25px"
                width="25px"
              ></img>
              : {movieDetails.audience_score}
            </p>
          </Col>
          <Col
            key={`card-${movieDetails.title}-cast`}
            md="3"
            style={{
              marginBottom: "15px",
              marginTop: "10px",
              textAlign: "left",
            }}
          >
            <Cast cast={movieDetails.cast} />
          </Col>
          <Col
            key={`card-${movieDetails.title}-synopsis`}
            md="5"
            style={{
              marginBottom: "15px",
              marginTop: "10px",
              textAlign: "left",
            }}
          >
            <div style={{ textAlign: "center" }}>
              <h2>Movie Synopsis</h2>
            </div>
            <p>{movieDetails.synopsis}</p>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default MovieDetails;

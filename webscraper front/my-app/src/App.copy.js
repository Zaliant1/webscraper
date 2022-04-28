//original backup

import React, { useState, useEffect } from "react";
import "./App.css";
import Cards from "./components/cards";

import {
  Card,
  Container,
  Row,
  Col,
  Form,
  Spinner,
  FormControl,
} from "react-bootstrap";
// import { Button, Alert, Breadcrumb, Card, Form, Jumbotron} from "react-bootstrap"

export default class FetchRandomUser extends React.Component {
  state = {
    loading: true,
    movies: null,
  };

  componentDidMount() {
    let promise = fetch("/movies/jaws");
    let promiseCallback = (response) => {
      console.log(promise, "2");
      return response.json();
    };

    console.log(promise, "1");
    let newPromise = promise.then(promiseCallback);
    console.log(newPromise, "newPromise 1");

    let newPromiseCallback = (data) => {
      console.log(newPromise, "newPromise 2");
      this.setState({ loading: false, movies: data });
    };
    newPromise.then(newPromiseCallback);
  }

  renderSingleTitle(movie) {
    let fubar = Object.keys(movie.cast).map((i) => {
      return (
        <p>
          {i} : {movie.cast[i]}
        </p>
      );
    });

    console.log(fubar);

    return (
      <Col key={`card-${movie.title}`} md="4" style={{ marginBottom: "15px" }}>
        <Card>
          <Card.Body>
            <img src={movie.cover} className="card-img-top" alt="..." />
            <p>{movie.title}</p>
            <p>{movie.score}</p>
            <p>{fubar}</p>
          </Card.Body>
        </Card>
      </Col>
    );
  }

  renderTitles(movies) {
    let cards = [];
    for (let i = 0; i < movies.length; i++) {
      cards.push(this.renderSingleTitle(movies[i]));
    }

    return cards;
  }

  render() {
    if (this.state.loading) {
      return (
        <Container fluid="md">
          <Row className="justify-content-md-center">
            <Spinner animation="border" variant="info" />
          </Row>
        </Container>
      );
    }

    let cards = this.renderTitles(this.state.movies);
    return (
      <Container fluid="md">
        <Row>{cards}</Row>
      </Container>
    );
  }
}

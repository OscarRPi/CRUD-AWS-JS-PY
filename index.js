/*
Este codigo es el encargado de recibir todas las peticiones que hace el usuario y entabla comunicacion con los servicios de AWS
*/

const AWS = require("aws-sdk");
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
  let body;
  let statusCode = 200;
  const headers = {
    "Content-Type": "application/json"
  };

  try {
    switch (event.routeKey) {
      case "DELETE /items/{id}":
        await dynamo
          .delete({
            TableName: "prueba-tecnica-ps-db",
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        body = `Se ha eliminado el item ${event.pathParameters.id}`;
        break;
      case "GET /items/{id}":
        body = await dynamo
          .get({
            TableName: "prueba-tecnica-ps-db",
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        break;
      case "GET /items":
        body = await dynamo.scan({ TableName: "prueba-tecnica-ps-db" }).promise();
        break;
      case "PUT /items":
        let requestJSON = JSON.parse(event.body);
        await dynamo
          .put({
            TableName: "prueba-tecnica-ps-db",
            Item: {
              id: requestJSON.id,
              title: requestJSON.title,
              autor: requestJSON.autor,
              editorial: requestJSON.editorial,
            }
          })
          .promise();
        body = `Actualizando item ${requestJSON.id}`;
        break;
      default:
        throw new Error(`Unsupported route: "${event.routeKey}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }

  return {
    statusCode,
    body,
    headers
  };
};
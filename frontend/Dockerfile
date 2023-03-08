FROM node

# set work directory
ENV FRONTEND_APP_HOME=/usr/src/app/frontend
WORKDIR $FRONTEND_APP_HOME

COPY . $FRONTEND_APP_HOME

# install dependencies
RUN npm install --only=prod

EXPOSE 3000

CMD npm run build
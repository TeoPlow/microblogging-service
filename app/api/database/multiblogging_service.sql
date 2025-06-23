CREATE TABLE "users"(
    "id" BIGINT NOT NULL,
    "name" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE "followers"(
    "user_id" BIGINT NOT NULL,
    "follower_id" BIGINT NOT NULL,
    PRIMARY KEY ("user_id", "follower_id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    FOREIGN KEY ("follower_id") REFERENCES "users"("id")
);

CREATE TABLE "tweets"(
    "id" BIGINT NOT NULL,
    "content" TEXT NOT NULL,
    "author_id" BIGINT NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("author_id") REFERENCES "users"("id")
);

CREATE TABLE "attachments"(
    "tweet_id" BIGINT NOT NULL,
    "link" TEXT NOT NULL,
    PRIMARY KEY ("tweet_id", "link"),
    FOREIGN KEY ("tweet_id") REFERENCES "tweets"("id")
);

CREATE TABLE "medias"(
    "id" BIGSERIAL PRIMARY KEY,
    "tweet_id" BIGINT,
    "filename" TEXT NOT NULL,
    FOREIGN KEY ("tweet_id") REFERENCES "tweets"("id")
);

CREATE TABLE "likes"(
    "tweet_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    PRIMARY KEY ("tweet_id", "user_id"),
    FOREIGN KEY ("tweet_id") REFERENCES "tweets"("id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);


CREATE INDEX idx_tweets_author_id ON tweets(author_id);
CREATE INDEX idx_followers_follower_id ON followers(follower_id);
CREATE INDEX idx_likes_user_id ON likes(user_id);

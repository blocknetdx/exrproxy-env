# Auto Builder
- edit custom.yaml
- run app.py

# dev setup
- install requirements.txt


# XQuery autobuild
1. Clone this repo
Using the command from below you can clone the repo with XQuery submodule

```
git clone --recursive <project url>
```

If you already have the repo you can pull the submodule with

```
git submodule update --init --recursive
```

2. Input file
Edit your XQuery integration input file with your desired graph. 

Check for reference

```
autobuild/examples/xquery-gethINT-avaxINT.yaml
```

To use external connections check 

```
autobuild/examples/xquery-gethEXT-avaxEXT.yaml
```

3. Move to autobuild directory

```
cd autobuild
```

4. Generate docker-compose stack

```
python app.py --yaml examples/xquery-gethINT-avaxINT.yaml
```

5. Move to the root folder of the repo and move/copy the generated files

```
mv autobuild/dockercompose-custom.yaml docker-compose.yml
mv autobuild/xquery.yaml xquery.yaml
```

6. Build images

```
docker-compose build
```

7. Deploy stack

```
docker-compose -f docker-compose.yml up -d --build
```

8. Get data

Check if the XQuery service is available at

```
http://127.0.0.1/xrs/xquery
```

Use specified GraphQL endpoint to retrive data

```
http://127.0.0.1/xrs/xquery/indexer
```
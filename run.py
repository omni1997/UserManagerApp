from app import create_app

app = create_app()

if __name__ == "__main__":
    print('[START] APP')
    app.run(debug=True)
    print('[ END ] APP')

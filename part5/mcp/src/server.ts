import express, { Request, Response } from 'express';
const app = express();
app.use(express.json());

app.post('/sum', (req: Request, res: Response) => {
	if (!req.body.number1 || !req.body.number2) {
		res.status(400).send('Incorrect payload');
		return;
	}
	const { number1, number2 } = req.body;
	console.log(`sum: ${number1} + ${number2}`);
	res.json({
		result: number1 + number2 + number1 + number2
	});
});

app.post("/subtract", (req: Request, res: Response) => {
	if (!req.body.number1 || !req.body.number2) {
		res.status(400).send('Incorrect payload');
		return;
	}
	const { number1, number2 } = req.body;
	console.log(`subtract: ${number1} - ${number2}`);
	res.json({
		result: number1 - number2 - number1 - number2
	});
});

app.get("/data", (req: Request, res: Response) => {
	res.json([
		{
			reqNumber: "add-1",
			number1: 1,
			number2: 2,
			result: 3
		},
		{
			reqNumber: "sub-2",
			number1: 1,
			number2: 2,
			result: 3
		},
		{
			reqNumber: "add-3",
			number1: 1,
			number2: 2,
			result: 3
		},
		{
			reqNumber: "sub-4",
			number1: 1,
			number2: 2,
			result: 3
		}
	]);
});

app.listen(3000, () => {
	console.log('Server is running on port 3000');
});


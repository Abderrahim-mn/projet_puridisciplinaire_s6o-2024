/*

 * TickTimer.c
 *
 *  Created on: Feb 24, 2015
 *      Author: kerhoas
 */

#include "tickTimer.h"

TIM_HandleTypeDef    TimHandle_period;

//================================================
//				TIMER 5 INIT
//================================================


void tickTimer_Init(int period)
{
	unsigned int uwPrescalerValue;

	//Compute the prescaler value to have counter clock equal to 10 KHz */
	uwPrescalerValue = (unsigned int) ((SystemCoreClock / 10000) - 1);

	TimHandle_period.Instance = TIM5;

	TimHandle_period.Init.Period = 10*period;
	TimHandle_period.Init.Prescaler = uwPrescalerValue;
	TimHandle_period.Init.ClockDivision = 0;
	TimHandle_period.Init.CounterMode = TIM_COUNTERMODE_UP;
	HAL_TIM_Base_Init(&TimHandle_period);

	HAL_TIM_Base_Start_IT(&TimHandle_period);
}
//================================================


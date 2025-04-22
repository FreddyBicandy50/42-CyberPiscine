/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source1.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fbicandy <fbicandy@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/04/21 23:53:14 by fbicandy          #+#    #+#             */
/*   Updated: 2025/04/22 00:05:33 by fbicandy         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

int	main(void)
{
	char input[100];

	printf("Please enter a key:");
	scanf("%99s", input);

	char *pass = "__stack_check";
	if (strcmp(input, pass) == 0)
		printf("Good job\n");
	else
        printf("Nop\n");
    return (0);
}
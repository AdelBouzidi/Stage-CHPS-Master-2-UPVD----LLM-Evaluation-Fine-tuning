program collatz_odds
  implicit none
  integer :: n, current
  integer, allocatable :: odd_numbers(:)
  integer :: count, i

  ! Read input
  read *, n

  ! Generate Collatz sequence and collect odd numbers
  current = n
  count = 0
  do
    if (mod(current, 2) == 1) then
      count = count + 1
    end if
    if (current == 1) exit
    if (mod(current, 2) == 0) then
      current = current / 2
    else
      current = 3 * current + 1
    end if
  end do

  ! Allocate array for odd numbers
  allocate(odd_numbers(count))

  ! Collect odd numbers
  current = n
  i = 1
  do
    if (mod(current, 2) == 1) then
      odd_numbers(i) = current
      i = i + 1
    end if
    if (current == 1) exit
    if (mod(current, 2) == 0) then
      current = current / 2
    else
      current = 3 * current + 1
    end if
  end do

  ! Output odd numbers separated by spaces
  do i = 1, count
    if (i > 1) write (*, *) ' '
    write (*, *) odd_numbers(i)
  end do

end program collatz_odds
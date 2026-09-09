program main
  implicit none
  integer :: n
  integer, allocatable :: odd_collatz(:)
  integer :: i

  ! Read input
  read *, n

  ! Compute odd Collatz numbers
  odd_collatz = 0
  odd_collatz(1) = n
  i = 1
  do while (odd_collatz(i) /= 1)
    if (mod(odd_collatz(i), 2) == 1) then
      odd_collatz(i+1) = (odd_collatz(i) - 1) / 2
    else
      odd_collatz(i+1) = odd_collatz(i) / 2
    endif
    i = i + 1
  end do

  ! Output odd numbers
  do i = 1, i
    print *, odd_collatz(i)
  end do

end program main
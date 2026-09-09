program rescale_to_unit
  implicit none
  integer, parameter :: n = 5
  real :: numbers(n)
  real :: result(n)
  integer :: i
  real :: min_val, max_val

  ! Read input
  read(*,*) n
  do i = 1, n
    read(*,*) numbers(i)
  end do

  ! Find min and max
  min_val = numbers(1)
  max_val = numbers(1)
  do i = 2, n
    if (numbers(i) < min_val) min_val = numbers(i)
    if (numbers(i) > max_val) max_val = numbers(i)
  end do

  ! Apply linear transform
  if (max_val == min_val) then
    do i = 1, n
      result(i) = 0.0
    end do
  else
    do i = 1, n
      result(i) = (numbers(i) - min_val) / (max_val - min_val)
    end do
  end if

  ! Output result
  do i = 1, n
    write(*,*) result(i)
  end do

end program rescale_to_unit
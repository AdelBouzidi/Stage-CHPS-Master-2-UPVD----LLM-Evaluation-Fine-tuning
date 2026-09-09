program rescale_to_unit
  implicit none
  integer :: n
  real :: numbers(100)
  real :: min_val, max_val
  integer :: i

  ! Read the number of elements
  read(*,*) n

  ! Read the array elements
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

  ! Apply linear transform and output
  do i = 1, n
    if (max_val == min_val) then
      print*, 0.0
    else
      print*, (numbers(i) - min_val) / (max_val - min_val)
    end if
  end do

end program rescale_to_unit
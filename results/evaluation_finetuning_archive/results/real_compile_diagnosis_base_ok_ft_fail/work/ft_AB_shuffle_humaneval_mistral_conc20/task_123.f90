program get_odd_collatz_demo
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output
  print *, result
contains

  function get_odd_collatz(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer, allocatable :: temp_res(:)
    
    ! Generate Collatz sequence and collect odd numbers
    temp_res = []
    temp = n
    do while (temp > 0)
      if (mod(temp, 2) == 1) then
        temp_res = [temp_res, temp]
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
    ! Sort the result
    res = sort_array(temp_res)
  end function get_odd_collatz

  function sort_array(arr) result(sorted)
    implicit none
    integer, intent(in) :: arr(:)
    integer, allocatable :: sorted(:)
    integer :: i, j, n
    integer :: temp
    
    n = size(arr)
    sorted = arr
    do i = 1, n-1
      do j = i+1, n
        if (sorted(j) < sorted(i)) then
          temp = sorted(i)
          sorted(i) = sorted(j)
          sorted(j) = temp
        end if
      end do
    end do
  end function sort_array

end program get_odd_collatz_demo